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

			puts { <h1><table class="blind"><td class="wide">WebUI QuickAccess</td><td><img src="backgrounds/yellow_teddybear.png" alt="Yellow Teddybear Software" class="titleimage"></td></table></h1> }

			set pin ""
			catch { import pin }
			set tablet ""
			catch { import tablet } 
				

			array set res [rega_script {

				boolean tablet = ("} $tablet {"=="1");

				if (tablet) { WriteLine ('<div class="clear"></div><table class="tablet">'); }
				
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

						if (tablet) { WriteLine ('<tr><th>'); }

						Write ('<div class="clear"></div><a name="' # s_loop_id # '"></a><h3><table class="blind"><td class="wide">');
						if (s_loop_id == ID_ROOMS) {
							Write ("Räume");
						} else {
							Write ("Gewerke");
						}
						WriteLine ('</td><td><div class="toparrow" onclick="jumptotop();"></div></td></table></h3>');

						if (tablet) { WriteLine ('</th><td>'); }
			
						foreach (s_object_id, dom.GetObject(s_loop_id).EnumUsedIDs()) {
							o_object = dom.GetObject (s_object_id);
							s_temp = o_object.Name();
							if (s_temp.Length() > 11) {
								s_temp = s_temp.Substr (0, 10) # ".";
							}
							Write('<a href="javascript:jumpto(\'channels.cgi?list=' # o_object.ID() # '&ianchor=' # s_loop_id # '\');"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">');
							WriteXML (s_temp);
							WriteLine ('</div></a>');
						}
						WriteLine ("");
						
						if (tablet) { WriteLine ('</td></tr>'); }
						
					}	

					
					if (tablet) { WriteLine ('<tr><th>'); }
					
					WriteLine ('<div class="clear"></div><a name="0"></a><h3><table class="blind"><td class="wide">Software/Hardware</td><td><div class="toparrow" onclick="jumptotop();"></div></td></table></h3>');
					
					if (tablet) { WriteLine ('</th><td>'); }
					
					WriteLine ('<a href="javascript:jumpto(\'software.cgi?list=programs&ianchor=0\');"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Programme</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'software.cgi?list=sysvar&ianchor=0\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">System-<br>variable</div></span></a>');
					WriteLine ('<a href="javascript:jumpto(\'directaccess.cgi?&ianchor=0\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Direct<br>Access</div></a></span>');
					WriteLine ('<a href="javascript:jumpto(\'hardware.cgi?ianchor=0\');"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Geräte</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'errors.cgi?ianchor=0\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Service-<br>meldungen</div></span></a>');
					WriteLine ('<span class="multi_4"><div class="standard"><span id="errors_count">offene<br>Meldungen<br>werden<br>gesucht</span></div></span>');
					WriteLine ("");

					if (tablet) { WriteLine ('</td></tr><tr><th>'); }

					WriteLine ('<div class="clear"></div><a name="1"></a><h3><table class="blind"><td class="wide">Einstellungen</td><td><div class="toparrow" onclick="jumptotop();"></div></td></table></h3>');
					
					if (tablet) { WriteLine ('</th><td>'); }
					
					WriteLine ('<script language="javascript" type="text/javascript">ColsSelection();</script>');
					WriteLine ('<script language="javascript" type="text/javascript">TabletSelection();</script>');
					WriteLine ('<script language="javascript" type="text/javascript">UpdateSelection();</script>');
					WriteLine ('<a href="javascript:jumpto(\'password.cgi\');"><div class="standard button' # (s_sys_pin != '') # '">PIN</div></a>');
					WriteLine ('<script language="javascript" type="text/javascript">AppSelection();</script>');
					WriteLine ('<a href="javascript:jumpto(\'help/index.htm\');"><div class="standard buttonhelp">Hilfe</div></a>');
					WriteLine ("");
					
					if (tablet) { WriteLine ('</td></tr><tr><th>'); }

					WriteLine ('<div class="clear"></div><a name="2"></a><h3><table class="blind"><td class="wide">Tools</td><td><div class="toparrow" onclick="jumptotop();"></div></td></table></h3>');
					
					if (tablet) { WriteLine ('</th><td>'); }
					
					WriteLine ('<a href="javascript:jumpto(\'tools_signatur.cgi?ianchor=2\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Signatur-<br>generator</div></span></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_inventur.cgi?ianchor=2\');"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Inventur</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_rooms.cgi?ianchor=2\');"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Räume</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_functions.cgi?ianchor=2\');"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Gewerke</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'tools_reboot.cgi?ianchor=2\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">CCU<br>neustarten</div></span></a>');
					WriteLine ('<script language="javascript" type="text/javascript">WebUIButton();</script>');
					
					WriteLine ("");
					
					if (tablet) { WriteLine ('</td></tr>'); }
					
				} ! PIN

				if (tablet) { WriteLine ('</table>'); }
				
			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { </div> }
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }

			
			puts { <script async src="errors-js.cgi" type="text/javascript"></script> }

		}

    }


}
