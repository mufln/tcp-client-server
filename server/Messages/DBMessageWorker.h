//
// Created by MuFln on 16.05.2024.
//

#ifndef TCP_CLIENT_SERVER_IMESSAGEWORKER_H
#define TCP_CLIENT_SERVER_IMESSAGEWORKER_H

#include "IDBMessageWorkerEssential.h"
class DBMessageWorker: public IDBMessageWorkerEssential{
public:
    void GetMessage() override;
    void PostMessage() override;
};


#endif //TCP_CLIENT_SERVER_IMESSAGEWORKER_H
