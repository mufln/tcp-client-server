cmake_minimum_required(VERSION 3.26)
project(tcp_client_server)

set(CMAKE_CXX_STANDARD 23)
add_executable(tcp_client_server server/main.cpp)
target_link_libraries(tcp_client_server pqxx)
target_include_directories(tcp_client_server PRIVATE ${server})
target_include_directories(tcp_client_server PRIVATE ${server/Autorization})
target_include_directories(tcp_client_server PRIVATE ${server/Messages})