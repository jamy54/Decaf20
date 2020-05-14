	# standard Decaf preamble 
	  .text
	  .align 2
	  .globl main
  _factorial:
	# BeginFunc 36
	  subu $sp, $sp, 8	# decrement sp to make space to save ra, fp
	  sw $fp, 8($sp)	# save fp
	  sw $ra, 4($sp)	# save ra
	  addiu $fp, $sp, 8	# set up new fp
	  subu $sp, $sp, 36	# decrement sp to make space for locals/temps
	# _tmp0 = 1
	  li $t2, 1		# load constant value 1 into $t2
	  sw $t2, -8($fp)	# spill _tmp0 from $t2 to $fp-8
	# _tmp1 = n < _tmp0
	  lw $t0, 4($fp)	# fill n to $t0 from $fp+4
	  lw $t1, -8($fp)	# fill _tmp0 to $t1 from $fp-8
	  slt $t2, $t0, $t1	
	  sw $t2, -12($fp)	# spill _tmp1 from $t2 to $fp-12
	# _tmp2 = n == _tmp0
	  lw $t0, 4($fp)	# fill n to $t0 from $fp+4
	  lw $t1, -8($fp)	# fill _tmp0 to $t1 from $fp-8
	  seq $t2, $t0, $t1	
	  sw $t2, -16($fp)	# spill _tmp2 from $t2 to $fp-16
	# _tmp3 = _tmp1 || _tmp2
	  lw $t0, -12($fp)	# fill _tmp1 to $t0 from $fp-12
	  lw $t1, -16($fp)	# fill _tmp2 to $t1 from $fp-16
	  or $t2, $t0, $t1	
	  sw $t2, -20($fp)	# spill _tmp3 from $t2 to $fp-20
	# IfZ _tmp3 Goto _L0
	  lw $t0, -20($fp)	# fill _tmp3 to $t0 from $fp-20
	  beqz $t0, _L0	# branch if _tmp3 is zero 
	# _tmp4 = 1
	  li $t2, 1		# load constant value 1 into $t2
	  sw $t2, -24($fp)	# spill _tmp4 from $t2 to $fp-24
	# Return _tmp4
	  lw $t2, -24($fp)	# fill _tmp4 to $t2 from $fp-24
	  move $v0, $t2		# assign return value into $v0
	  move $sp, $fp		# pop callee frame off stack
	  lw $ra, -4($fp)	# restore saved ra
	  lw $fp, 0($fp)	# restore saved fp
	  jr $ra		# return from function
  _L0:
	# _tmp5 = 1
	  li $t2, 1		# load constant value 1 into $t2
	  sw $t2, -28($fp)	# spill _tmp5 from $t2 to $fp-28
	# _tmp6 = n - _tmp5
	  lw $t0, 4($fp)	# fill n to $t0 from $fp+4
	  lw $t1, -28($fp)	# fill _tmp5 to $t1 from $fp-28
	  sub $t2, $t0, $t1	
	  sw $t2, -32($fp)	# spill _tmp6 from $t2 to $fp-32
	# PushParam _tmp6
	  subu $sp, $sp, 4	# decrement sp to make space for param
	  lw $t0, -32($fp)	# fill _tmp6 to $t0 from $fp-32
	  sw $t0, 4($sp)	# copy param value to stack
	# _tmp7 = LCall _factorial
	  jal _factorial     	# jump to function
	  move $t2, $v0		# copy function return value from $v0
	  sw $t2, -36($fp)	# spill _tmp7 from $t2 to $fp-36
	# PopParams 4
	  add $sp, $sp, 4	# pop params off stack
	# _tmp8 = n * _tmp7
	  lw $t0, 4($fp)	# fill n to $t0 from $fp+4
	  lw $t1, -36($fp)	# fill _tmp7 to $t1 from $fp-36
	  mul $t2, $t0, $t1	
	  sw $t2, -40($fp)	# spill _tmp8 from $t2 to $fp-40
	# Return _tmp8
	  lw $t2, -40($fp)	# fill _tmp8 to $t2 from $fp-40
	  move $v0, $t2		# assign return value into $v0
	  move $sp, $fp		# pop callee frame off stack
	  lw $ra, -4($fp)	# restore saved ra
	  lw $fp, 0($fp)	# restore saved fp
	  jr $ra		# return from function
	# EndFunc
	# (below handles reaching end of fn body with no explicit return)
	  move $sp, $fp		# pop callee frame off stack
	  lw $ra, -4($fp)	# restore saved ra
	  lw $fp, 0($fp)	# restore saved fp
	  jr $ra		# return from function
  main:
	# BeginFunc 48
	  subu $sp, $sp, 8	# decrement sp to make space to save ra, fp
	  sw $fp, 8($sp)	# save fp
	  sw $ra, 4($sp)	# save ra
	  addiu $fp, $sp, 8	# set up new fp
	  subu $sp, $sp, 48	# decrement sp to make space for locals/temps
	# _tmp9 = 1
	  li $t2, 1		# load constant value 1 into $t2
	  sw $t2, -12($fp)	# spill _tmp9 from $t2 to $fp-12
	# n = _tmp9
	  lw $t2, -12($fp)	# fill _tmp9 to $t2 from $fp-12
	  sw $t2, -8($fp)	# spill n from $t2 to $fp-8
  _L1:
	# _tmp10 = 15
	  li $t2, 15		# load constant value 15 into $t2
	  sw $t2, -16($fp)	# spill _tmp10 from $t2 to $fp-16
	# _tmp11 = n < _tmp10
	  lw $t0, -8($fp)	# fill n to $t0 from $fp-8
	  lw $t1, -16($fp)	# fill _tmp10 to $t1 from $fp-16
	  slt $t2, $t0, $t1	
	  sw $t2, -20($fp)	# spill _tmp11 from $t2 to $fp-20
	# _tmp12 = n == _tmp10
	  lw $t0, -8($fp)	# fill n to $t0 from $fp-8
	  lw $t1, -16($fp)	# fill _tmp10 to $t1 from $fp-16
	  seq $t2, $t0, $t1	
	  sw $t2, -24($fp)	# spill _tmp12 from $t2 to $fp-24
	# _tmp13 = _tmp11 || _tmp12
	  lw $t0, -20($fp)	# fill _tmp11 to $t0 from $fp-20
	  lw $t1, -24($fp)	# fill _tmp12 to $t1 from $fp-24
	  or $t2, $t0, $t1	
	  sw $t2, -28($fp)	# spill _tmp13 from $t2 to $fp-28
	# IfZ _tmp13 Goto _L2
	  lw $t0, -28($fp)	# fill _tmp13 to $t0 from $fp-28
	  beqz $t0, _L2	# branch if _tmp13 is zero 
	# _tmp14 = "Factorial("
	  .data			# create string constant marked with label
	  _string1: .asciiz "Factorial("
	  .text
	  la $t2, _string1	# load label
	  sw $t2, -32($fp)	# spill _tmp14 from $t2 to $fp-32
	# PushParam _tmp14
	  subu $sp, $sp, 4	# decrement sp to make space for param
	  lw $t0, -32($fp)	# fill _tmp14 to $t0 from $fp-32
	  sw $t0, 4($sp)	# copy param value to stack
	# LCall _PrintString
	  jal _PrintString   	# jump to function
	# PopParams 4
	  add $sp, $sp, 4	# pop params off stack
	# PushParam n
	  subu $sp, $sp, 4	# decrement sp to make space for param
	  lw $t0, -8($fp)	# fill n to $t0 from $fp-8
	  sw $t0, 4($sp)	# copy param value to stack
	# LCall _PrintInt
	  jal _PrintInt      	# jump to function
	# PopParams 4
	  add $sp, $sp, 4	# pop params off stack
	# _tmp15 = ") = "
	  .data			# create string constant marked with label
	  _string2: .asciiz ") = "
	  .text
	  la $t2, _string2	# load label
	  sw $t2, -36($fp)	# spill _tmp15 from $t2 to $fp-36
	# PushParam _tmp15
	  subu $sp, $sp, 4	# decrement sp to make space for param
	  lw $t0, -36($fp)	# fill _tmp15 to $t0 from $fp-36
	  sw $t0, 4($sp)	# copy param value to stack
	# LCall _PrintString
	  jal _PrintString   	# jump to function
	# PopParams 4
	  add $sp, $sp, 4	# pop params off stack
	# PushParam n
	  subu $sp, $sp, 4	# decrement sp to make space for param
	  lw $t0, -8($fp)	# fill n to $t0 from $fp-8
	  sw $t0, 4($sp)	# copy param value to stack
	# _tmp16 = LCall _factorial
	  jal _factorial     	# jump to function
	  move $t2, $v0		# copy function return value from $v0
	  sw $t2, -40($fp)	# spill _tmp16 from $t2 to $fp-40
	# PopParams 4
	  add $sp, $sp, 4	# pop params off stack
	# PushParam _tmp16
	  subu $sp, $sp, 4	# decrement sp to make space for param
	  lw $t0, -40($fp)	# fill _tmp16 to $t0 from $fp-40
	  sw $t0, 4($sp)	# copy param value to stack
	# LCall _PrintInt
	  jal _PrintInt      	# jump to function
	# PopParams 4
	  add $sp, $sp, 4	# pop params off stack
	# _tmp17 = "\n"
	  .data			# create string constant marked with label
	  _string3: .asciiz "\n"
	  .text
	  la $t2, _string3	# load label
	  sw $t2, -44($fp)	# spill _tmp17 from $t2 to $fp-44
	# PushParam _tmp17
	  subu $sp, $sp, 4	# decrement sp to make space for param
	  lw $t0, -44($fp)	# fill _tmp17 to $t0 from $fp-44
	  sw $t0, 4($sp)	# copy param value to stack
	# LCall _PrintString
	  jal _PrintString   	# jump to function
	# PopParams 4
	  add $sp, $sp, 4	# pop params off stack
	# _tmp18 = 1
	  li $t2, 1		# load constant value 1 into $t2
	  sw $t2, -48($fp)	# spill _tmp18 from $t2 to $fp-48
	# _tmp19 = n + _tmp18
	  lw $t0, -8($fp)	# fill n to $t0 from $fp-8
	  lw $t1, -48($fp)	# fill _tmp18 to $t1 from $fp-48
	  add $t2, $t0, $t1	
	  sw $t2, -52($fp)	# spill _tmp19 from $t2 to $fp-52
	# n = _tmp19
	  lw $t2, -52($fp)	# fill _tmp19 to $t2 from $fp-52
	  sw $t2, -8($fp)	# spill n from $t2 to $fp-8
	# Goto _L1
	  b _L1		# unconditional branch
  _L2:
	# EndFunc
	# (below handles reaching end of fn body with no explicit return)
	  move $sp, $fp		# pop callee frame off stack
	  lw $ra, -4($fp)	# restore saved ra
	  lw $fp, 0($fp)	# restore saved fp
	  jr $ra		# return from function
