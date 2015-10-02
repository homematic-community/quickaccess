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

			puts { <script src="style.js" type="text/javascript"></script> }

			puts { <h1 class="maintitle">WebUI QuickAccess</h1> }
			puts { <img src="yellow_teddybear.png" alt="Yellow Teddybear Software" class="titleimage"> }
			puts { <p class="newline"></p> }

			set pin ""
			catch { import pin }

			array set res [rega_script {

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {
				
					string s_loop = ID_ROOMS # "\t" # ID_FUNCTIONS # "\t";
					string s_loop_id;
					object o_object;
					string s_object_id;
					string s_temp;

					foreach (s_loop_id, s_loop) {
						Write ('<h3><a name="' # s_loop_id # '">');
						if (s_loop_id == ID_ROOMS) {
							Write ("Räume");
						} else {
							Write ("Gewerke");
						}
						WriteLine ('</a></h3>');
			
						foreach (s_object_id, dom.GetObject(s_loop_id).EnumUsedIDs()) {
							o_object = dom.GetObject (s_object_id);
							s_temp = o_object.Name();
							if (s_temp.Length() > 11) {
								s_temp = s_temp.Substr (0, 10) # ".";
							}
							Write('<a href="javascript:jumpto(\'channels.cgi?list=' # o_object.ID() # '&ianchor=' # s_loop_id # '\');"><div onclick="this.className=\'active\';" class="buttonfalse">');
							WriteXML (s_temp);
							WriteLine ('</div></a>');
						}
						WriteLine ("");
					}	

					WriteLine ('<h3><a name="0">Software/Hardware</a></h3>');
					WriteLine ('<a href="javascript:jumpto(\'software.cgi?list=programs&ianchor=0\');"><div onclick="this.className=\'active\';" class="buttonfalse">Programme</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'software.cgi?list=sysvar&ianchor=0\');"><span class="multi_2"><div onclick="this.className=\'active\';" class="buttonfalse">System-<br>variable</div></span></a>');
					WriteLine ('<a href="javascript:jumpto(\'directaccess.cgi?&ianchor=0\');"><span class="multi_2"><div onclick="this.className=\'active\';" class="buttonfalse">Direct<br>Access</div></a></span>');
					WriteLine ('<a href="javascript:jumpto(\'hardware.cgi?ianchor=0\');"><div onclick="this.className=\'active\';" class="buttonfalse">Geräte</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'errors.cgi?ianchor=0\');"><span class="multi_2"><div onclick="this.className=\'active\';" class="buttonfalse">Service-<br>meldungen</div></span></a>');
					WriteLine ('<span class="multi_4"><div><span id="errors_count">offene<br>Meldungen<br>werden<br>gesucht</span></div></span>');
					WriteLine ("");

					WriteLine ('<h3><a name="1">Einstellungen</a></h3>');
					WriteLine ('<script language="javascript" type="text/javascript">ColsSelection();</script>');
					WriteLine ('<script language="javascript" type="text/javascript">UpdateSelection();</script>');
					WriteLine ('<a href="javascript:jumpto(\'password.cgi\');"><div class="button' # (s_sys_pin != '') # '">PIN</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'help/index.htm\');"><div class="buttonhelp">Hilfe</div></a>');
					WriteLine ("");
					
					WriteLine ('<h3><a name="2">Tools</a></h3>');
					WriteLine ('<a href="javascript:jumpto(\'tools_signatur.cgi?ianchor=2\');"><span class="multi_2"><div onclick="this.className=\'active\';" class="buttonfalse">Signatur-<br>generator</div></span></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_inventur.cgi?ianchor=2\');"><div onclick="this.className=\'active\';" class="buttonfalse">Inventur</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_rooms.cgi?ianchor=2\');"><div onclick="this.className=\'active\';" class="buttonfalse">Räume</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_functions.cgi?ianchor=2\');"><div onclick="this.className=\'active\';" class="buttonfalse">Gewerke</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_reboot.cgi?ianchor=2\');"><span class="multi_2"><div onclick="this.className=\'active\';" class="buttonfalse">CCU<br>neustarten</div></span></a>');
					WriteLine ("");
				} ! PIN

			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2014 by Yellow Teddybear Software</p> }

			
			puts { <script src="errors-js.cgi" type="text/javascript"></script> }

		}

    }


}
