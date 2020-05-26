#!/usr/bin/env python
# -*- coding: utf-8 -*-
# apt install mpg123

formantit = {
"vokaali" : {
#         F1   F2    F3    F4    t
	"a": [788, 1246, 2854, 3916, 0.09],
	"e": [530, 2430, 3104, 4299, 0.12],
	"i": [328, 2928, 3701, 4317, 0.11],
	"o": [537, 964,  2642, 3880, 0.09],
	"u": [364, 498, 2755, 3893, 0.15],
	"y": [314, 1589, 2544, 3984, 0.13],
	"å": [537, 964,  2642, 3880, 0.09],
	"ä": [948, 2037, 2812, 4004, 0.14],
	"ö": [460, 1737, 2768, 3928, 0.135]
	},
"konsonantti" :{
	"b": [195, 1636, 2655, 3898, 0.09],
	"c": [1299, 2346, 3551, 4320, 0.12], 
	"d": [483, 1749, 2710, 3777, 0.08],
	"f": [1265, 2331, 3174, 4005, 0.12],
	"g": [373, 1155, 2772, 3304, 0.11], 
	"h": [978, 2606, 3156, 3929, 0.10],
	"j": [230, 2344, 3475, 4089, 0.08],
	"k": [520, 1988, 3232, 3476, 0.043],
	"l": [439, 1113, 2780, 3155, 0.13],
	"m": [257, 1365, 3156, 3343, 0.13],
	"n": [290, 1838, 2265, 3304, 0.11],
	"p": [574, 1109, 2856, 3954, 0.022],
	"q": [0.00001, 0, 0, 0, 0.00001],    
	"r": [536, 1260, 2521, 3902, 0.11],
	"s": [1765, 3058, 3999, 4557, 0.13],
	"t": [459, 2491, 3145, 4313, 0.033],
	"v": [216, 1221, 2660, 3688, 0.1],
	"w": [238, 1033, 2850, 3992, 0.12],
	"x": [1232, 2610, 3708, 4394, 0.14],      
	"z": [1273, 2547, 3578, 4432, 0.14],     
	" ": [0.00001,0,0,0,0.125],
	".": [0.00001,0,0,0,0.25],          
	",": [0.00001,0,0,0,0.25],
	";": [0.00001,0,0,0,0.25],
	":": [0.00001,0,0,0,0.25],    
	"ng": [303, 1781, 2992, 3639, 0.2]
	},   

"diftongi" : {                                         
	"ai": [437, 1787, 2856, 4192, 0.3],
	"ei": [424, 2603, 3182, 4403, 0.3],
	"oi": [415, 1715, 2890, 4093, 0.3],
	"ui": [339, 1464, 2958, 4073, 0.3],
	"yi": [334, 2258, 2935, 4109, 0.3],
	"äi": [680, 2279, 2843, 4224, 0.3],
	"öi": [431, 2241, 2885, 4144, 0.3],  
	"au": [621, 1068, 2637, 3797, 0.2],
	"eu": [466, 1751, 2983, 4084, 0.3],    
	"iu": [365, 1759, 3001, 4080, 0.3],
	"ei": [424, 2603, 3182, 4403, 0.3],
	"ou": [423, 865, 2818, 3698, 0.3],
	"äy": [670, 1726, 2748, 4098, 0.3],
	"öy": [409, 1664, 2733, 3866, 0.3],
	"iy": [329, 2268, 3015, 4061, 0.3],
	"ey": [401, 2151, 2940, 4087, 0.3],
	"ie": [460, 2588, 3248, 4360, 0.3],
	"uo": [406, 750, 2736, 3626, 0.3],
    "yö": [368, 1774, 2608, 3624, 0.3]
	},

"aakkoset" : {
	"aa": [707, 1230, 2753, 3882, 0.2],
	"ee": [550, 2428, 3118, 4319, 0.26],
	"ii": [330, 2928, 3678, 4333, 0.17],
	"oo": [532, 945, 2659, 3855, 0.19],
	"uu": [351, 611, 2858, 3838, 0.3],
	"yy": [296, 1672, 2536, 4071, 0.25],
	"åå": [532, 945, 2659, 3855, 0.19],
	"ää": [909, 2152, 2896, 4042, 0.3],
	"öö": [478, 1670, 2768, 3979, 0.27]
	}
}  
