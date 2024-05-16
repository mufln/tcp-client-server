//
// Created by MuFln on 16.05.2024.
//

#ifndef TCP_CLIENT_SERVER_IDBWORKER_H
#define TCP_CLIENT_SERVER_IDBWORKER_H

#include <pqxx/pqxx>
#include <iostream>
class IDBWorker {
protected:
    std::string address;
    std::string port;
    connection conn;
public:
    virutal void Connect() = 0;
    virtual void Close() = 0;
};


#endif //TCP_CLIENT_SERVER_IDBWORKER_H
