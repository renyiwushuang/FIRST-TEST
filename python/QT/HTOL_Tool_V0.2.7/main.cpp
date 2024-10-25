#include "mainwindow.h"

#include <QApplication>
#include "logical_data_processing/test_module_exception_handle.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    //SetUnhandledExceptionFilter(errCallback);
    return a.exec();
}
