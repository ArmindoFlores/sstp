#ifndef _IPC_H_
#define _IPC_H_

#include <future>
#include <string>
#include <thread>
#include <vector>

namespace SSTP {
    class IPCServer {
    public:
        IPCServer(const std::string& socket_path);
        ~IPCServer();
        
        bool setup();
        bool main_loop();
        void stop();
        void process_client_connection(int clientfd);

    private:
        std::string socket_path;
        int socketfd;
        std::vector<std::thread> active_threads;
        std::vector<std::future<void>> active_futures;
    };
}

#endif