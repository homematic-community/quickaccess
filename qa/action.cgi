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

			set id ""
			set action ""
			catch { import id }
			catch { import action }
			set pin ""
			catch { import pin }

			array set res [rega_script {

				! PARAMETER
				object o_object = dom.GetObject("} $id {");
				string s_action = "} $action {";

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					WriteLine ('<h1>Aktivität</h1>');


					Write ('<h3>');
					WriteXML (o_object.Name())
					WriteLine ('</h3>');

					WriteLine ('<span class="multi_2"><div>Aktion<br>' # s_action # '</div></span>');

					o_object.State(s_action);

					WriteLine ('<script type="text/javascript"> jumpto ("channels.cgi#" + js_anchor); </script>');
					
				}

			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2014 by Yellow Teddybear Software</p> }



		}

    }

}
