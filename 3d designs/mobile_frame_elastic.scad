difference(){
    difference(){
        cube([200,115,35]);
        translate([9.5, 9.5, 0])
        cube([181,96,30]);
        translate([2, 2, 1])
        cube([196,111,32]);
        translate([130, 0, 10])
        cube([60,3,15]);
        translate([5, 0, 10])
        cube([80,3,15]);
    }

    translate([195, 57.5, 20])
    rotate([0,90,0])
    cylinder(r=6.5, h=10);
    translate([195, 10, 0])
    cube([10,3,8]);
    translate([195, 15, 0])
    cube([10,3,8]);
    translate([195, 20, 0])
    cube([10,3,8]);
    }
    