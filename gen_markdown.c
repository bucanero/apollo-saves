#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SAVE_TYPE   "PS3"
#define SAVE_FOLDER "PS3"

void save_main(char* path, char* title)
{
    FILE * fp;
    FILE * out;
    char * line = NULL;
    char * pos;
    size_t len = 0;
    ssize_t read;
    char vmi[200];

    chdir(path);
    fp = fopen("saves.txt", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    out = fopen("README.md", "w");

    fprintf(out, "---\nlayout: default\ntitle: \"%s\"\nparent: " SAVE_TYPE " Saves\npermalink: " SAVE_FOLDER "/%s/\n---\n", title, path);
    fprintf(out, "# %s\n\n## " SAVE_TYPE " Saves - %s\n\n| Icon | Filename | Description |\n|------|----------|-------------|\n", title, path);

    while ((read = getline(&line, &len, fp)) != -1) {
		line[read-1] = 0;
		pos = strchr(line, '=');
		*pos = 0;
		
        fprintf(out, "| ![%s](ICON0.PNG) | [%s](%s){: .btn .btn-purple } | %s |\n", title, line, line, ++pos);
    }

    fclose(out);
    fclose(fp);
    if (line)
        free(line);

    chdir("..");
}

int main(int argc, char** argv)
{
    FILE * fp;
    char * line = NULL;
    char * pos;
    size_t len = 0;
    ssize_t read;

    fp = fopen("games.txt", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    printf("---\nlayout: default\ntitle: " SAVE_TYPE " Saves\npermalink: " SAVE_FOLDER "/\nhas_children: true\nhas_toc: false\n---\n");
    printf("# Games\n\n| Game | Title ID |\n|------|----------|\n");

    while ((read = getline(&line, &len, fp)) != -1) {
		line[read-1] = 0;
		pos = strchr(line, '=');
		*pos = 0;
        printf("| [%s](%s/) | %s |\n", ++pos, line, line);
        save_main(line, pos);
    }

    fclose(fp);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}
