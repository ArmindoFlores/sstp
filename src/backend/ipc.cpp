#include "ipc.h"
#include <algorithm>
#include <future>
#include <boost/json/src.hpp>
#include <sys/socket.h>
#include <sys/un.h>
#include <iostream>

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
        std::thread thread([this, clientfd]{ this->process_client_connection(clientfd); });
        thread.detach();
        // std::packaged_task<void()> task([this, clientfd]{ this->process_client_connection(clientfd); });
        // active_futures.push_back(task.get_future());
        // active_threads.emplace_back(std::move(task));
    }

    // for (size_t i = 0; i < active_futures.size(); i++) {
    //     if (active_futures[i].wait_for(std::chrono::seconds(0)) == std::future_status::ready) {
    //         (void) active_futures[i].get();
    //         active_threads[i].join();
    //     }
    // }

    // std::remove_if(active_futures.begin(), active_futures.end(), [](const std::future<void>& future){ return !future.valid(); });
    // std::remove_if(active_threads.begin(), active_threads.end(), [](const std::thread& thread){ return !thread.joinable(); });
    
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

    std::cout << value << std::endl;
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