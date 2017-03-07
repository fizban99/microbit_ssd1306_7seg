micropython library to emulate a 7 segment display on a OLED SSD1306 128x64 I2C with a micro:bit
################################################################################################

This library allows the micro:bit to emulate a 7 segment display with the typical low cost 0,96" OLED display sold in Amazon and eBay connected to the default I2C pins of the micro:bit. Some sort of breakout is required. Note that the Kitronik breakout does not have pre-soldered the I2C pins and you will need to attach some headers to access the I2C pins.

You should connect the device's SCL pin to micro:bit pin 19, and the device's SDA pin to micro:bit pin 20. You also must connect the device's ground to the micro:bit ground (pin GND). 

This library uses the full resolution of the display, since it does not use a display buffer. All segments have been designed not to overlap the area of another segment. Number rendering is really fast, since only segments that change are drawn or cleared and the segments have been defined to expand to as few pages as possible. 

The library requires a binary definition of the segments to be loaded (segments.bin) together with the ssd1306_7seg.py file. This allows reducing memory consumption at compile time.


   .. image:: 7segments.png
      :width: 100%
      :align: center


.. contents::

.. section-numbering::


Main features
=============

* 128x64 resolution of the numbers
* 4 digits 
* Option to draw two dots to separate the first two digits from the second two digits to display times
* Sample program demonstrating the usage



   .. image:: microbit_timer.jpg
      :width: 100%
      :align: center

Library usage
=============


initialize(showDots, showZeros)
+++++++++++++++++++++++++++++++


Initializes the OLED display with zeros if showZeros is set to 1 and with two dots separating the first two digits to display times if showDots is set to 1. 

.. code-block:: python

   from SSD1306_7seg import initialize 
   
   initialize(1,1)


disp_num(n, numDec=0)
+++++++++++++++++++++


Displays the number n on the screen, with the decimal point at position numDec, being 0 the right-most position. n should be between 0 and 9999. If numDec=0 no decimal point is displayed. Note that the digit 0 does not support decimal point.

.. code-block:: python

   from SSD1306_7seg import initialize, disp_num 
   
   initialize(1,1)
   disp_num(1306)


set_digit(dig, d)
+++++++++++++++++


   .. image:: 7-segment.png
      :width: 100%
      :align: center

Displays the digit definition *d* at position *digit*. A digit definition is created as the resulting binary number of the combination of required segments to paint the number:


   .. image:: bit_table.png
      :width: 100%
      :align: center


According to the above table, to paint a 1 we have to use the value 0x60 at the desired position. If we want digit 0 to be 1, we would use:


.. code-block:: python

   from SSD1306_7seg import initialize, set_digit 
   
   initialize(0,0)
   set_digit(0,0x60)

Can you make the display show HELO? You can find the hexadecimal codes in the excel file of the tools folder.
