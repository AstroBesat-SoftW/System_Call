#include <unistd.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <sys/types.h> 
#include <sys/wait.h> 
void gotoxy(int x,int y) 
{ 
printf("%c[%d;%df",0x1B,y,x); 
} 
int main (void){ 
pid_t f; 
int status,sutun=1; 
printf("Program çalışıyor: Kimliğim= %d\n", getpid()); 
f=fork(); 
if (f==0) /*çocuk*/ 
{ 
} 
sutun=45; sleep(4); 
gotoxy(sutun,4);    printf("Ben çocuk. Kimliğim= %d", getpid()); 
gotoxy(sutun,5);    printf("Annemin kimliği= %d", getppid()); 
//exit(0); 
else if (f>0)/* anne */ 
{ 
sleep(1); 
printf("\nBen anne. Kimliğim= %d", getpid()); 
printf("\nAnnemin kimliği= %d", getppid()); 
printf("\nÇocuğumun kimliği= %d\n", f); 
if (waitpid(f, &status, 0) == -1) { 
perror("waitpid"); 
} 
sleep(2); 
//exit(0); 
} 
gotoxy(sutun,7); printf("Bitti."); 
gotoxy(sutun,8); printf("-------------------------------"); 
exit(0); 
}
