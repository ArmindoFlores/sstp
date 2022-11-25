#include "ipc.h"
#include <boost/json/src.hpp>
#include <algorithm>
#include <future>
#include <iostream>
#include <sstream>
#include <sys/socket.h>
#include <sys/un.h>

SSTP::IPCServer::IPCServer(const std::string& socket_path) : socket_path(socket_path), socketfd(-1) {}
SSTP::IPCServer::~IPCServer()
{
    stop();
}

bool SSTP::IPCServer::setup()
{
    struct sockaddr_un address;

    socketfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (socketfd < 0) {
        return false;
    }

    address.sun_family = AF_UNIX;
    std::strcpy(address.sun_path, socket_path.c_str());

    if (bind(socketfd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        close(socketfd);
        return false;
    }

    if (listen(socketfd, 5) < 0) {
        close(socketfd);
        return false;
    }
    return true;
}

bool SSTP::IPCServer::main_loop()
{
    struct sockaddr_un address;
    socklen_t l = sizeof(address);
    std::cout << "Accepting connections..." << std::endl;
    int clientfd = accept(socketfd, (struct sockaddr*)&address, &l);
    if (clientfd > 0) {
        std::cout << "Got new connection, spinning up new thread" << std::endl;
        std::thread thread([this, clientfd]{ this->process_client_connection(clientfd); close(clientfd); });
        thread.detach();
    }
    return true;
}

void SSTP::IPCServer::process_client_connection(int fd)
{
    std::stringstream ss;
    char buffer[1024] = "";
    ssize_t nread = 0;
    while ((nread = read(fd, buffer, sizeof(buffer)-1)) > 0) {
        buffer[nread] = 0;
        ss << buffer;
        if (buffer[nread-1] == '\0')
            break;
    }

    if (nread <= 0) {
        std::cout << "Client disconnected prematurely" << std::endl;
        return;
    }

    std::string request(ss.str());
    std::cout << "Received all data" << std::endl;
    std::cout << request << std::endl;

    boost::json::error_code ec;
    boost::json::value value = boost::json::parse(request, ec);
    
    if (ec.failed()) {
        std::cout << "Failed to parse JSON" << std::endl;
        return;
    }    

    std::string response = process_command(value);
    size_t total_sent = 0;
    int n_sent = 0;
    while (total_sent < response.length() && (n_sent = write(fd, response.c_str()+total_sent, response.length()-total_sent)) > 0) {
        total_sent += n_sent;
    }
}

std::optional<boost::json::value> SSTP::IPCServer::get_command(bool wait)
{
    if (!wait) {
        std::unique_lock<std::mutex> lock(queue_mutex);
        if (command_queue.size() > 0) {
            boost::json::value result = command_queue.front();
            command_queue.pop();
            return result;
        }
        return {};
    }
    std::unique_lock<std::mutex> lock(queue_mutex);
    while (command_queue.size() == 0) { queue_cv.wait(lock); }
    boost::json::value result = command_queue.front();
    command_queue.pop();
    return result;
}

SSTP::SolarSystem& SSTP::IPCServer::solar_system()
{
    return ss;
}

std::string SSTP::IPCServer::process_command(const boost::json::value& cmd)
{      
    if (!cmd.is_object())
        return "";

    auto main_object = cmd.as_object();

    if (!main_object.contains("type"))
        return "";

    if (!main_object["type"].is_string())
        return "";

    std::string cmd_type {main_object["type"].as_string().c_str()};
    if (cmd_type == "get_planet_positions") {
        boost::json::array positions;
        for (auto& body : ss.get_planets()) {
            auto position = body.position();
            boost::json::array p_array(3);
            p_array[0] = position[0];
            p_array[1] = 0;
            p_array[2] = position[1];
            positions.push_back(p_array);
        }
        std::string response = boost::json::serialize(positions);
        return response;
    }
    return "";
}

void SSTP::IPCServer::stop()
{
    // for (size_t i = 0; i < active_threads.size(); i++) {
    //     active_threads[i].join();
    // }

    unlink(socket_path.c_str());
    if (socketfd >= 0) {
        close(socketfd);
    }
}