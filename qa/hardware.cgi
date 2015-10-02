#!/bin/tclsh

load tclrega.so
source [file join $env(DOCUMENT_ROOT) once.tcl]
source [file join $env(DOCUMENT_ROOT) cgi.tcl]



cgi_eval {
	

	cgi_input
	cgi_content_type "text/html; charset=iso-8859-1"
	cgi_http_head

    cgi_html {

		cgi_head {
    		cgi_title "HomeMatic QuickAccess"
			puts { <link href="style.css" rel="stylesheet" type="text/css"> }
			puts { <meta name="viewport" content="width=device-width, initial-zoom=1" /> }
		}

		cgi_body {

			set pin ""
			catch { import pin }

			puts { <script src="style.js" type="text/javascript"></script> }

			array set res [rega_script {

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					string s_hss_list;
					string s_device;
					string s_subdevice;
					string s_temp;
					string tab = '\t';
					string done = 'ZZZZZZZZZZ';

					foreach (s_device, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
						s_device = dom.GetObject(s_device).HssType();
						if ((s_hss_list.Find (s_device # tab) < 0)) {
							s_temp = "";
							foreach (s_subdevice, s_hss_list) {
								if (s_subdevice > s_device) {
									s_temp = s_temp # s_device # tab;
									s_device = done;
								} 
								s_temp = s_temp # s_subdevice # tab;
							}
							if (s_device != done) {
								s_temp = s_temp # s_device # tab;
							}
							s_hss_list = s_temp;
						}
					}

					WriteLine ('<h1>Geräte</h1>');
					WriteLine ('<a href="javascript:jumpto(\'index.cgi#\' + js_ianchor);"><div onclick="this.className=\'active\';" class="button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="button">abmelden</div></a>');
					}
					WriteLine ('<a href="javascript:jumpto(\'help/hardware.htm\');"><div class="buttonhelp">Hilfe</div></a>');
					WriteLine ('<h3></h3>');

					integer i_pointer;
					integer i_subpointer;
					integer i_lines;

					foreach (s_device, s_hss_list) {
						s_subdevice = s_device;
						i_pointer = 8;
						i_subpointer = 0;
						i_lines = 1;
						s_temp = '';
						while (i_subpointer < s_subdevice.Length()) {
							if (s_subdevice.Substr (i_subpointer, 1) == '-') {
								i_pointer = i_subpointer;
							}
							i_subpointer = i_subpointer + 1;
							if (i_subpointer > 8) {
								s_temp = s_temp # s_subdevice.Substr (0, i_pointer + 1) # '<br />';
								s_subdevice = s_subdevice.Substr (i_pointer + 1, (s_subdevice.Length() - i_pointer) - 1);
								i_subpointer = 0;
								i_pointer = 8;
								i_lines = i_lines + 1;
							}
						}
						s_subdevice = s_temp # s_subdevice;

						WriteLine('<a href="javascript:jumpto(\'channels.cgi?list=' # s_device # '\');"><span class="multi_' # i_lines # '"><div onclick="this.className=\'active\';" class="buttonfalse">' # s_subdevice # '</div></span></a>');
					}

				}
					
			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2014 by Yellow Teddybear Software</p> }


		}

    }


}
