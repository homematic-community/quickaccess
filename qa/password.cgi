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
    		cgi_title "PIN - HomeMatic QuickAccess"
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

			set pin ""
			set newpin ""
			catch { import pin }
			catch { import newpin }

			array set res [rega_script {

				! TITEL
				WriteLine ('<h1>PIN</h1>');

				! PARAMETER
				string s_pin = "} $pin {";
				string s_newpin = "} $newpin {";

				! SYSTEMVARIABLE
				object o_sysvars = dom.GetObject (ID_SYSTEM_VARIABLES);
				object o_sys_pin = dom.GetObject ('QuickAccess PIN');
				string s_uniquename;
				if (!o_sys_pin) {
					if ((o_sysvars) && (dom.CheckName ('QuickAccess PIN', &s_uniquename, ID_SYSTEM_VARIABLES))) {
						o_sys_pin = dom.CreateObject (OT_VARDP);
						o_sys_pin.Name ('QuickAccess PIN');
						o_sysvars.Add (o_sys_pin.ID());
						o_sys_pin.DPInfo ("");
						o_sys_pin.ValueType (ivtString);
						o_sys_pin.ValueSubType (istChar8859);
						o_sys_pin.State("");
					}
				}

				! VARIABLE
				integer i_temp;
				string s_pinname;
				string s_formname;
				string s_subtext;
				
				! FALSCHE PIN
				if ((o_sys_pin.Value() != "") && (s_pin.ToInteger() != (o_sys_pin.Timestamp() - o_sys_pin.Value().ToInteger()))) {
				
					if (s_pin == "logout") {
						o_sys_pin.State (o_sys_pin.Value());
						s_pin = "";
					}
				
					WriteLine ('<div class="clear"></div><h3>QuickAccess ist gesperrt</h3>');
					s_pinname = 'pin';
					s_subtext = '<p>Geben Sie die PIN ein und bestätigen Sie mit OK. Wenn Sie die PIN nicht mehr wissen, löschen Sie in der WebUI die Systemvariable "QuickAccess PIN".</p>' #
								'<p>Speichern Sie diese Seite in Ihren Bookmarks ab, wenn Sie bei jedem Aufruf nach der PIN gefragt werden wollen.</p>';
					
				! RICHTIGE PIN
				} else {

					! PIN LÖSCHEN
					if (s_newpin == "void") {
						o_sys_pin.State ("");
						s_newpin = "";
						WriteLine ('<script language="javascript" type="text/javascript">jumpto (\'password.cgi?pin=void\');</script>');
					} 

					! PIN ÄNDERN (AKTION)
					if (s_newpin != "") {
						o_sys_pin.State (o_sys_pin.Timestamp().ToInteger() - s_newpin.ToInteger());
						s_pin = o_sys_pin.Timestamp().ToInteger() - o_sys_pin.Value().ToInteger();
						WriteLine ('<script language="javascript" type="text/javascript">jumpto (\'password.cgi?pin=' # s_pin # '\');</script>');
					}

					! PIN ÄNDERN (FORMULAR)
					if (s_newpin == "") {
					
						WriteLine ('<a href="javascript:jumpto(\'index.cgi\');"><span class="multi_1"><div onclick="this.className=\'standard active\';" class="standard button">Startseite</div></span></a>');
						if (o_sys_pin.Value() != "") {
							WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><span class="multi_1"><div onclick="this.className=\'standard active\';" class="standard button">abmelden</div></span></a>');
							WriteLine ('<a href="javascript:jumpto(\'password.cgi?newpin=void\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard button">PIN<br>löschen</div></span></a>');
						}
						WriteLine ('<a href="javascript:jumpto(\'help/password.htm\');"><div class="standard buttonhelp">Hilfe</div></a>');

						WriteLine ('<div class="clear"></div><h3>PIN ändern</h3>');
						WriteLine ('<p>Geben Sie eine neue PIN ein, und bestätigen Sie die neue PIN mit OK. Sie können ohne PIN-Änderung zur Startseite wechseln.</p>');
						s_pinname = 'newpin';
						s_subtext = '<p>Bitte beachten Sie: Die PIN ist lediglich eine einfache Kindersicherung.</p>' #
									'<p>Wenn Sie QuickAccess in Ihren Bookmarks speichern, wird die PIN im Klartext abgespeichert. Klicken Sie oben auf "abmelden", und speichern Sie die Paßwortabfrage in Ihren Bookmarks. Wenn "QuickAccess ist gesperrt" angezeigt wird, wird die PIN nicht mit in Ihren Bookmarks abgespeichert, und Sie werden beim Aufruf nach der PIN gefragt.</p>' #
									'<p>Wenn Ihre Besucher Ihren Browser-Verlauf betrachten, können sie die PIN im Klartext sehen. Löschen Sie den Verlauf, um Ihre PIN geheim zu halten.</p>';
					}

				}

				! JAVASCRIPT-BASIS ZUR PIN"VERSCHLÜSSELUNG"
				s_formname = 'document.formular.' # s_pinname # '.value';
				WriteLine ('<script language="JavaScript">');
				WriteLine ('  var js_pin_base=' # o_sys_pin.Timestamp().ToInteger() # ';');
				WriteLine ('  function submit_form() {');
				WriteLine ('    ' # s_formname # ' = js_pin_base - parseInt (' # s_formname # '.replace(/\D/g, ""));');
				WriteLine ('    document.formular.submit();');
				WriteLine ('  }');
				WriteLine ('</script>');
				

				WriteLine ('<form name="formular" method="get" action="password.cgi" onsubmit="submit_form();">');
				WriteLine ('<script language="javascript" type="text/javascript">HiddenFormFields(["cols", "anchor", "counter", "tablet", "app"]);</script>');
				if (s_pinname != "pin") {
					WriteLine ('<input type="hidden" name="pin" value="' # s_pin # '" />');
				}
				WriteLine ('<div class="standard inputfield"><input class="standard inputfield" type="input" name="' # s_pinname # '" value=""/></div>');
				WriteLine ('</form>');

				WriteLine ('<div class="clear"></div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'1\';" class="standard button">1</div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'2\';" class="standard button">2</div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'3\';" class="standard button">3</div>');
				WriteLine ('<div class="clear"></div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'4\';" class="standard button">4</div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'5\';" class="standard button">5</div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'6\';" class="standard button">6</div>');
				WriteLine ('<div class="clear"></div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'7\';" class="standard button">7</div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'8\';" class="standard button">8</div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'9\';" class="standard button">9</div>');
				WriteLine ('<div class="clear"></div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '.substr (0, ' # s_formname # '.length - 1);" class="standard button">&lt;</div>');
				WriteLine ('<div onclick="' # s_formname # '=' # s_formname # '+\'0\';" class="standard button">0</div>');
				WriteLine ('<a href="javascript:submit_form();"><div onclick="this.className=\'standard active\';" class="standard button">OK</div></a>');
				WriteLine ('<div class="clear"></div>');

				WriteLine (s_subtext);
				

			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { </div> }
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }



		}


	}

}
