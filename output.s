.text
factorial:
subu $sp,$sp,32
sw $ra,20($sp)
sw $fp,16($sp)
addiu $fp,$sp,28
sw $a0,0($fp)
lw $t0,0($fp)
li $t1,1
slt $t2,$t0,$t1
seq $t3,$t0,$t1
or $t2,$t2,$t3
beqz $t2,L1
li $v0,1
lw $ra, 20($sp)
lw $fp, 16($sp)
addiu $sp, $sp, 32 
jr $ra
L1:
li $t4,1
sub $t0,$t0,$t4
move $a1,$t0
sw $t0,0($fp)
sw $t1,4($fp)
sw $t2,8($fp)
sw $t3,12($fp)
sw $t4,16($fp)
jal factorial
lw $t4,16($fp)
lw $t3,12($fp)
lw $t2,8($fp)
lw $t1,4($fp)
lw $t0,0($fp)
mul $t0,$t0,$v0
move $v0,$t0
lw $ra, 20($sp)
lw $fp, 16($sp)
addiu $sp, $sp, 32 
jr $ra
.text
.globl main
main:
subu $sp,$sp,32
sw $ra,20($sp)
sw $fp,16($sp)
addiu $fp,$sp,28
li $t1,1
move $t0,$t1
L3:
li $t2,15
slt $t3,$t0,$t2
seq $t4,$t0,$t2
or $t3,$t3,$t4
beqz $t3,L2
.data
$jam4:
.ascii "Factorial("
.text
la $t5,$jam4
move $a0,$t5
li $v0,4
syscall
move $a0,$t0
li $v0,1
syscall
.data
$jam5:
.ascii ") = "
.text
la $t6,$jam5
move $a0,$t6
li $v0,4
syscall
move $a0,$t0
sw $t0,0($fp)
sw $t1,4($fp)
sw $t2,8($fp)
sw $t3,12($fp)
sw $t4,16($fp)
sw $t5,20($fp)
sw $t6,24($fp)
jal factorial
lw $t6,24($fp)
lw $t5,20($fp)
lw $t4,16($fp)
lw $t3,12($fp)
lw $t2,8($fp)
lw $t1,4($fp)
lw $t0,0($fp)
move $a0,$v0
li $v0,1
syscall
.data
$jam6:
.ascii "\n"
.text
la $t7,$jam6
move $a0,$t7
li $v0,4
syscall
li $t8,1
add $t0,$t0,$t8
move $t9,$t0
move $t0,$t9
b L3
L2:
lw $ra, 20($sp)
lw $fp, 16($sp)
addiu $sp, $sp, 32 
li $v0, 10
syscall
