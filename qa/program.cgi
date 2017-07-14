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
    		cgi_title "Programm - HomeMatic QuickAccess"
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

					! VARIABLE
					
					boolean b_directaccess;
					string s_temp;
					string s_directaccess_new;
				
					! SYSTEMVARIABLE FÜR DIRECTACCESS EINRICHTEN
					
					string s_uniquename;
					string s_directaccess = "QuickAccess DirectAccess";
					object o_SysVars = dom.GetObject (ID_SYSTEM_VARIABLES);
					object o_directaccess = dom.GetObject (s_directaccess);
					if (!o_directaccess) {
						if ((o_SysVars) && (dom.CheckName (s_directaccess, &s_uniquename, ID_SYSTEM_VARIABLES))) {
							o_directaccess = dom.CreateObject (OT_VARDP);
							o_directaccess.Name (s_directaccess);
							o_SysVars.Add (o_directaccess.ID());
							o_directaccess.DPInfo ("");
							o_directaccess.ValueType (ivtString);
							o_directaccess.ValueSubType (istChar8859);
							o_directaccess.State(":");
						}
					}					

					WriteLine ("<h1>Programmstart</h1>");
					
					! PROGRAMM AUSFÜHREN
					
					if (s_action == "run") {				
						Write ('<div class="clear"></div><h3>');
						WriteXML (o_object.Name());
						WriteLine ('</h3>');
						o_object.ProgramExecute();
						WriteLine ('<script type="text/javascript"> jumpto ("software.cgi?list=programs"); </script>');
					} else {
					
						! MENÜ ANZEIGEN
					
						WriteLine ('<a href="javascript:jumpto(\'software.cgi?list=programs\');"><div onclick="this.className=\'standard active\';" class="standard button">zurück</div></a>');
						if (s_sys_pin != "") {
							WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="standard button">abmelden</div></a>');
						}
						WriteLine ('<a href="javascript:jumpto(\'help/program.htm\');"><div class="standard buttonhelp">Hilfe</div></a>');

						s_directaccess = o_directaccess.Value();
						if ((s_action == 'da_true') || (s_action == 'da_false')) {
							s_directaccess_new = ":";
							foreach (s_temp, s_directaccess.Split (':')) {
								if ((s_temp != '') && (s_temp != o_object.ID().ToString())) {
									s_directaccess_new = s_directaccess_new # s_temp # ':';
								}
							}
							if (s_action == 'da_true') {
								s_directaccess_new = s_directaccess_new # o_object.ID() # ':';
								WriteLine ('<span class="multi_2"><div class="standard">DirectAccess<br>eingerichtet</div></span>');
							} else {
								WriteLine ('<span class="multi_2"><div class="standard">DirectAccess<br>entfernt</div></span>');
							}
							o_directaccess.State (s_directaccess_new);
							s_directaccess = s_directaccess_new;
						}

						Write ('<div class="clear"></div><h3>');
						WriteXML (o_object.Name());
						WriteLine ('</h3>');
						WriteLine ('<script type="text/javascript">document.title = "' # o_object.Name() # ' - HomeMatic QuickAccess";</script>');						
						WriteLine ('<a href="javascript:jumpto(\'program.cgi?id=' # o_object.ID() # '&action=run\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard button">Programm<br>ausführen</div></span></a>');

						s_directaccess = o_directaccess.Value();
						b_directaccess = (s_directaccess.Find (':' # o_object.ID() # ':') >= 0);
						WriteLine ('<a href="javascript:jumpto(\'program.cgi?id=' # o_object.ID() # '&action=da_' # (!b_directaccess) # '\');"><div onclick="this.ClassName=\'standard active\';" class="standard button' # b_directaccess # '">DirectAccess</div></a>');
					}
					
				}

			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { </div> }
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }



		}


	}

}
