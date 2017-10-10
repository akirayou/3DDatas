# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:26:47 2016

@author: akira
"""

import sys
import math
theD=0.2

lastE=None
absmode=True
px=0
py=0
pe=0
lastAngle=None
lasteLength=None
lines=sys.stdin.readlines()

for line in lines:
    line=line.rstrip()
    
    if(len(line)==0 or line[0]!='G'):
        #print(line)
        continue
    cmd=line.split()
    dcmd=dict()
    for c in cmd:
        if( not c[0] in dcmd):dcmd[c[0]]=c[1:]
    cmd=dcmd

    cmd['G']=int(cmd['G'])
 
    if('X' in cmd):cmd['X']=float(cmd['X'])
    if('Y' in cmd):cmd['Y']=float(cmd['Y'])
    if('E' in cmd):cmd['E']=float(cmd['E'])



    
    if cmd['G'] == 90:
        absmode=True
    if cmd['G'] == 91:
        absmode=False
    if cmd['G'] == 92:
        if('X' in cmd):px=cmd['X']
        if('Y' in cmd):py=cmd['Y']
        if('E' in cmd):pe=cmd['E']

    if cmd['G'] in [0,1,2,3]:
        nx=cmd['X'] if 'X' in cmd else px
        ny=cmd['Y'] if 'Y' in cmd else py
        
    if(cmd['G'] in[0,1]):
        dx=nx-px
        dy=ny-py
        angle=math.atan2(dx,dy)
        length=math.hypot(dx,dy)
        
        if( ('E' in cmd) and (not lastE is None) and ( (absmode and cmd['E']-lastE>1e-10)or( (not absmode) and cmd['E']>1e-10))  and length>1e-10 ): 
            #correction
            diffAngle=angle-lastAngle;
            if(diffAngle<0):diffAngle+=math.pi*2
            if(math.pi<diffAngle):diffAngle=math.pi*2-diffAngle
            halfTheta=diffAngle/2
            if( lastLength<1e-10):halfTheta=0
            
            eZeroLen=(math.tan(halfTheta)-halfTheta)*theD/4;            
            print(";;correct ",halfTheta/math.pi)
            print(";;correct cut ",eZeroLen/length*100,"%")
            if(length<eZeroLen):
                eZeroLen=length
                sys.stderr("too short path",line)
            mx=eZeroLen*math.cos(angle)
            my=eZeroLen*math.sin(angle)
            me=0
            
            if(absmode):
                mx+=px
                my+=py
                me+=lastE
            option=""
            if('F' in cmd):option+=" F"+cmd['F']

            line=";;"+line                     
            print("G"+str(cmd['G']),'X'+str(mx),'Y'+str(my),option)  #no extrude here
            e=cmd['E']
            if(absmode):
                e-=lastE
                print("G92 E"+str(e*eZeroLen/length+lastE)) #skip E
            else:
                cmd['E']*=1-eZeroLen/length
            
            print("G"+str(cmd['G']),'X'+str(nx),'Y'+str(ny),'E'+str(cmd['E']),option)  #no extrude here

        
        lastE=cmd['E'] if ('E' in cmd) else None
        lastAngle=angle
        lastLength=length
        
        
        
    if cmd['G'] in [0,1,2,3]:
        px=nx
        py=ny
        
        
    print(line)
