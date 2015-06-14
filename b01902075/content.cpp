#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>

#define MAX 10000
char content[MAX];

int main(int argc, char* argv[]){
	FILE *input_file = fopen(argv[1], "r");
	FILE *output_file = fopen("course_content", "a+");
	while(fgets(content, MAX, input_file) != NULL){
		if(strcmp(content, "<課程識別碼>\n") == 0){
			fgets(content, MAX, input_file);
			fputs("<c>\n", output_file);
			fputs(content, output_file);
		}
		else if(strcmp(content, "<課程概述>\n") == 0){ // fgets eat newline??
			while(fgets(content, MAX, input_file) != NULL){
				if(strcmp(content, "</>\n") == 0) break;
				fputs(content, output_file);
			}
			break;
		}
	}
	if(ferror(input_file)){
		printf("the buffer is too small\n");
		exit(1);
	}

	fputs("</>\n", output_file);

	fclose(input_file);
	fclose(output_file);

	return 0;
}