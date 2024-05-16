//
// Created by MuFln on 16.05.2024.
//

#ifndef TCP_CLIENT_SERVER_IDBWORKERAUTORIZATION_H
#define TCP_CLIENT_SERVER_IDBWORKERAUTORIZATION_H

#include "../IDBWorker.h"
class IDBWorkerAutorization:public IDBWorker {
public:
    virtual void RegisterUser(string name, string password) = 0;
    virtual void Login(string username, string password) = 0;
};


#endif //TCP_CLIENT_SERVER_IDBWORKERAUTORIZATION_H
