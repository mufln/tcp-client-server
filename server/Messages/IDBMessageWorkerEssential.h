//
// Created by MuFln on 16.05.2024.
//

#ifndef TCP_CLIENT_SERVER_IMESSAGEWORKERESSENTIAL_H
#define TCP_CLIENT_SERVER_IMESSAGEWORKERESSENTIAL_H

#include "../IDBWorker.h"
class IDBMessageWorkerEssential:IDBWorker {
public:
    virtual void GetMessage() = 0;
    virtual void PostMessage() = 0;

};


#endif //TCP_CLIENT_SERVER_IMESSAGEWORKERESSENTIAL_H
