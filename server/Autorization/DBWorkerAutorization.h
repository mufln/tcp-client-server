//
// Created by MuFln on 16.05.2024.
//

#ifndef TCP_CLIENT_SERVER_DBWORKERAUTORIZATION_H
#define TCP_CLIENT_SERVER_DBWORKERAUTORIZATION_H

#include "IDBWorkerAutorization.h"
class DBWorkerAutorization:public IDBWorkerAutorization {
public:
    void RegisterUser(string username, string password) override;
    void Login(string username, string password) override;
};


#endif //TCP_CLIENT_SERVER_DBWORKERAUTORIZATION_H
