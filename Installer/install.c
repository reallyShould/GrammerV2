#include <stdio.h>
#include <curl/curl.h>
#include <string.h>

size_t write_data(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    size_t written = fwrite(ptr, size, nmemb, stream);
    if (written != size * nmemb) {
        fprintf(stderr, "Error writing data to file\n");
    }
    return written;
}

int download(char* url, char* path)
{
    CURL *curl;
    CURLcode res;
    FILE *fp;
    //char fullpath[FILENAME_MAX] = strcat(path, strtok());

    curl = curl_easy_init();
    if(curl) {
        fp = fopen("/home/reallys/GrammerV2/Installer/path", "wb");

        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);

        res = curl_easy_perform(curl);

        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));

        fclose(fp);
        curl_easy_cleanup(curl);
    }
    return 1;
}

int main() {
    FILE* urls;
    char* pathToInstall;
    char* api;
    char* userid;

    char str[] = "Geeks-for-Geeks";
 
    // Returns first token 
    char *token = strtok(str, "-");
   
    // Keep printing tokens while one of the
    // delimiters present in str[].
    printf("%d",  strtok(str, "-")[1]);
    while (token != NULL)
    {
        printf("%s\n", token);
        token = strtok(NULL, "-");
    }


    return 0;
}