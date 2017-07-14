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
    		cgi_title "Signatur - HomeMatic QuickAccess"
			puts { <link href="style.css" rel="stylesheet" type="text/css"> }
			puts { <meta name="viewport" content="width=960, initial-zoom=1" /> }
			puts { <meta name="format-detection" content="telephone=no" /> }
			puts { <link rel="apple-touch-icon" href="favicons/icon.png" /> }
			puts { <link rel="icon" href="favicons/icon.png" /> }
			puts { <link rel="shortcut icon" href="favicons/favicon.ico" /> }
			if { ![catch { import app }] } {
				if { $app == "1" } {
					puts { <meta name="mobile-web-app-capable" content="yes" /> }
					puts { <meta name="apple-mobile-web-app-capable" content="yes" /> }
 				}
			}

		}

		cgi_body {

			puts { <script src="style.js" type="text/javascript"></script> }
			puts { <div class="background"></div><div class="page"> }
			puts { <h1>Signatur&shy;generator</h1>}

			
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

					WriteLine ('<a href="javascript:jumpto(\'index.cgi#\' + js_ianchor);"><div onclick="this.className=\'standard active\';" class="standard button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="standard button">abmelden</div></a>');
					}

					string s_device;
					string s_channel;
					object o_device;
					integer i_devices = 0;
					integer i_channels = 0;

					string s_typelist = "";

					foreach(s_device, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
					  var o_device = dom.GetObject(s_device);
					  if ((o_device.Address() != "BidCoS-Wir") && (o_device.Address() != "BidCoS-RF") && 
						  (o_device.HssType() != "HM-Sec-SD-Team")) {
						i_devices = i_devices + 1;
						s_typelist = s_typelist # o_device.HssType () # "\t";
						foreach(s_channel, o_device.Channels().EnumUsedIDs()) {
						  i_channels = i_channels + 1;
						}
					  }
					}

					Write ('<p>');
					WriteXML(i_channels # " Kanäle in " # i_devices # " Geräten:");
					Write ('</p><p>');
					
					string s_typeidx;
					string s_typeidx2;
					string s_typechecked = "";
					integer i_subcount;
					foreach (s_typeidx, s_typelist) {
					  if (s_typechecked.Find(s_typeidx) == -1) {
					  i_subcount = 0;
					  foreach (s_typeidx2, s_typelist) {
						if (s_typeidx2 == s_typeidx) { 
						  i_subcount = i_subcount + 1; }
						}
						if (s_typechecked == "") { 
						  s_typechecked = i_subcount # "x " # s_typeidx; 
						} else { 
						  s_typechecked = s_typechecked # ", " # i_subcount # "x " # s_typeidx; 
						}
					  }
					}

					WriteXML (s_typechecked);

					Write('</p>');
		
					
				} ! PIN
					
			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }

		}

    }


}
