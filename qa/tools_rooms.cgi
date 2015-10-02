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
			puts {<h1>Räume</h1>}
			
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

					WriteLine ('<a href="javascript:jumpto(\'index.cgi#\' + js_ianchor);"><div onclick="this.className=\'active\';" class="button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="button">abmelden</div></a>');
					}

					string s;
					Write ('<pre>');
					foreach (s, dom.GetObject (ID_ROOMS).EnumUsedNames()) {
						WriteXML (s);
						WriteLine ('');
					}
					WriteLine ('</pre>');
				
				} ! PIN
					
			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010,2011 by Yellow Teddybear Software</p> }


		}

    }


}
