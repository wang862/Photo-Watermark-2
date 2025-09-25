// main.cpp - 程序入口点
#include <windows.h>
#include <iostream>
#include <string>

// 应用程序主窗口类声明
class MainWindow {
private:
    HWND hWnd; // 窗口句柄
    HINSTANCE hInstance; // 应用程序实例句柄

public:
    MainWindow(HINSTANCE hInst);
    ~MainWindow();
    bool Create();
    void Show(int nCmdShow);
    static LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);

private:
    void OnCreate();
    void OnPaint();
    void OnDestroy();
};

// MainWindow 类实现
MainWindow::MainWindow(HINSTANCE hInst) : hWnd(NULL), hInstance(hInst) {
}

MainWindow::~MainWindow() {
}

bool MainWindow::Create() {
    // 注册窗口类
    WNDCLASSEX wcex;
    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wcex.hCursor = LoadCursor(NULL, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = NULL;
    wcex.lpszClassName = TEXT("PhotoWatermarkApp");
    wcex.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wcex)) {
        MessageBox(NULL, TEXT("注册窗口类失败！"), TEXT("错误"), MB_ICONERROR);
        return false;
    }

    // 创建窗口
    hWnd = CreateWindowEx(
        0,
        TEXT("PhotoWatermarkApp"),
        TEXT("图片水印工具 - Photo Watermark 2"),
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, hInstance, this
    );

    if (!hWnd) {
        MessageBox(NULL, TEXT("创建窗口失败！"), TEXT("错误"), MB_ICONERROR);
        return false;
    }

    return true;
}

void MainWindow::Show(int nCmdShow) {
    ShowWindow(hWnd, nCmdShow);
    UpdateWindow(hWnd);
}

LRESULT CALLBACK MainWindow::WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    MainWindow* pThis;

    if (message == WM_NCCREATE) {
        // 保存this指针到窗口数据中
        CREATESTRUCT* pCreate = (CREATESTRUCT*)lParam;
        pThis = (MainWindow*)pCreate->lpCreateParams;
        SetWindowLongPtr(hWnd, GWLP_USERDATA, (LONG_PTR)pThis);
        pThis->hWnd = hWnd;
    } else {
        // 从窗口数据中获取this指针
        pThis = (MainWindow*)GetWindowLongPtr(hWnd, GWLP_USERDATA);
    }

    if (pThis) {
        switch (message) {
        case WM_CREATE:
            pThis->OnCreate();
            return 0;
        case WM_PAINT:
            pThis->OnPaint();
            return 0;
        case WM_DESTROY:
            pThis->OnDestroy();
            return 0;
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
        }
    }
    return DefWindowProc(hWnd, message, wParam, lParam);
}

void MainWindow::OnCreate() {
    // 窗口创建时的初始化代码
    // 这里将在后续实现中添加更多控件和功能
}

void MainWindow::OnPaint() {
    PAINTSTRUCT ps;
    HDC hdc = BeginPaint(hWnd, &ps);

    // 绘制欢迎信息
    RECT rect;
    GetClientRect(hWnd, &rect);
    DrawText(hdc, TEXT("欢迎使用图片水印工具！"), -1, &rect, DT_SINGLELINE | DT_CENTER | DT_VCENTER);

    EndPaint(hWnd, &ps);
}

void MainWindow::OnDestroy() {
    PostQuitMessage(0);
}

// 应用程序管理器类
class AppManager {
private:
    HINSTANCE hInstance;
    MainWindow* mainWindow;

public:
    AppManager(HINSTANCE hInst) : hInstance(hInst), mainWindow(NULL) {
    }

    ~AppManager() {
        if (mainWindow) {
            delete mainWindow;
            mainWindow = NULL;
        }
    }

    bool Initialize() {
        // 创建主窗口
        mainWindow = new MainWindow(hInstance);
        if (!mainWindow->Create()) {
            return false;
        }
        return true;
    }

    void Run(int nCmdShow) {
        // 显示主窗口
        mainWindow->Show(nCmdShow);

        // 消息循环
        MSG msg;
        while (GetMessage(&msg, NULL, 0, 0)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }
};

// WinMain - Windows程序入口点
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // 初始化应用程序管理器
    AppManager app(hInstance);
    if (!app.Initialize()) {
        return 1;
    }

    // 运行应用程序
    app.Run(nCmdShow);

    return 0;
}