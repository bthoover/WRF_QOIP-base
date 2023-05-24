load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
  A = addfile("./fcst.nc","rw")

 ist = 167
 jst = 62
 ied = 187
 jed = 82 
 vNames = (/ "MU" /)
 nNames = dimsizes (vNames)   ; Number of variables on the file

 do n=0, nNames-1              ; Loop through each variable
    va = A->$vNames(n)$        ; Read the variable to memory
;    vb = B->$vNames(n)$
    vc = new(dimsizes(va),typeof(va))
    vc!0 = va!0        ; BTH - set first variable dimension name of vc to same as va ("t")
    vc!1 = va!1        ; BTH - set second variable dim. name of vc to same as va ("j")
    vc!2 = va!2        ; BTH - set third variable dim. name of vc to same as va ("i")
    
    dims = dimsizes(vc)
    vc = 0.
    vc@_FillValue = 0.
    copyatt(vc,va)
    do j = jst-1, jed-1
       do i = ist-1, ied-1
          if ( vNames(n) .eq. "MU") then
             vc(0,j,i) = -1.0
          end if
       end do
    end do
   

    gName = "G_"+vNames(n) 
    A->$gName$ = vc
    delete(va)
    delete(vc)

 end do

end
