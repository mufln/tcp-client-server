//
// Created by MuFln on 16.05.2024.
//

#ifndef TCP_CLIENT_SERVER_IDBWORKERAUTORIZATION_H
#define TCP_CLIENT_SERVER_IDBWORKERAUTORIZATION_H

#include "../IDBWorker.h"
class IDBWorkerAutorization:public IDBWorker {
public:
    virtual RegisterUser(string name, string password) = 0;
    virtual Login(string username, string password);
};


#endif //TCP_CLIENT_SERVER_IDBWORKERAUTORIZATION_H
