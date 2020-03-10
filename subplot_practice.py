# -*- coding: utf-8 -*-

35.139238, 128.872537

from matplotlib import pyplot as plt
import pvlib
pvlib.solarposition

ax1 = plt.subplot(311)
ax2 = plt.subplot(323)
ax3 = plt.subplot(324)
ax4 = plt.subplot(325)
ax5 = plt.subplot(326)

'''
------------------------------------------
|                                         |
|                                         |
|                                         |
|                                         |
------------------------------------------

-------------------  ---------------------
|                  | |                    |
|                  | |                    |
|                  | |                    |
|                  | |                    |
-------------------  ---------------------

-------------------  ---------------------
|                  | |                    |
|                  | |                    |
|                  | |                    |
|                  | |                    |
-------------------  ---------------------

'''
fig = plt.figure(constrained_layout = True)
gs = fig.add_gridspec(8,8)
ax1 = fig.add_subplot(gs[0:2,0:5])
ax2 = fig.add_subplot(gs[0:4,5:])
ax3 = fig.add_subplot(gs[2:4,0:5])
ax4 = fig.add_subplot(gs[4:7,0:3],aspect = 'equal')
ax4.axis('off')
ax5 = fig.add_subplot(gs[4,3],aspect = 'equal')
ax5.axis('off')
ax6 = fig.add_subplot(gs[4:7,4:7],aspect = 'equal')
ax6.axis('off')
ax7 = fig.add_subplot(gs[4,7],aspect = 'equal')
ax7.axis('off')

plt.show()
