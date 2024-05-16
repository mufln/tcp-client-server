//
// Created by MuFln on 16.05.2024.
//

#ifndef TCP_CLIENT_SERVER_IDBWORKER_H
#define TCP_CLIENT_SERVER_IDBWORKER_H

#include <>
#include <iostream>
using namespace pqxx;
using namespace std;
class IDBWorker {
protected:
    std::string address;
    std::string port;
    connection conn;
public:
    virtual void Connect() = 0;
    virtual void Close() = 0;
};


#endif //TCP_CLIENT_SERVER_IDBWORKER_H
