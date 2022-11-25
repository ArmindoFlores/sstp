#ifndef _IPC_H_
#define _IPC_H_

#include <condition_variable>
#include <mutex>
#include <optional>
#include <queue>
#include <string>
#include <thread>

#include <boost/json.hpp>
#include "solarsys.h"

namespace SSTP {
    class IPCServer {
    public:
        IPCServer(const std::string& socket_path);
        ~IPCServer();
        
        bool setup();
        bool main_loop();
        void stop();
        void process_client_connection(int clientfd);
        std::optional<boost::json::value> get_command(bool wait=false);
        SolarSystem& solar_system();
        std::string process_command(const boost::json::value& cmd);

    private:
        SolarSystem ss;
        std::string socket_path;
        int socketfd;
        std::mutex queue_mutex;
        std::condition_variable queue_cv;
        std::queue<boost::json::value> command_queue;
    };
}

#endif