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

			set list ""
			catch { import list }
			set pin ""
			catch { import pin }
			set tablet ""
			catch { import tablet }
	
			array set res [rega_script {

				! PARAMETER
				string s_list = "} $list {";
				boolean tablet = ("} $tablet {"=="1");

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					if (s_list == 'programs') {
						WriteLine ('<h1>Programme</h1>');
						WriteLine ('<script type="text/javascript">document.title = "Programme - HomeMatic QuickAccess";</script>');
						s_list = ID_PROGRAMS;
					}
					if (s_list == 'sysvar') {
						WriteLine ('<h1>Systemvariable</h1>');
						WriteLine ('<script type="text/javascript">document.title = "Systemvariable - HomeMatic QuickAccess";</script>');
						s_list = ID_SYSTEM_VARIABLES;
					}
						
					WriteLine ('<a href="javascript:jumpto(\'index.cgi#0\');"><div onclick="this.className=\'standard active\';" class="standard button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="standard button">abmelden</div></a>');
					}
					WriteLine ('<a href="javascript:jumpto(\'help/software.htm\');"><div class="standard buttonhelp">Hilfe</div></a>');
					WriteLine ('<div class="clear"></div>');

					object o_object;
					string s_object_id;
					string s_text;
					string s_value;
					string tab = "\t";
					string splitchar=" .,-/_";
					integer i_length = 11;
					integer i_pointer;
					integer i_subpointer;
					integer i_count;
					string s_initial = '';
					boolean b_first = true;

					if (tablet) { WriteLine ('<table class="tablet">'); }
				
					foreach (s_object_id, dom.GetObject(s_list).EnumUsedIDs()) {
						o_object = dom.GetObject (s_object_id);

						if (o_object.Name().Substr(0,1) != s_initial) {
							if (tablet) { 
								if (!b_first) {
									WriteLine ('</td></tr>');
								} else {
									b_first = false;
								}
								WriteLine ('<tr><th>'); 
							}
							s_initial = o_object.Name().Substr(0,1);
							WriteLine ('<div class="clear"></div><h3 style="text-align:center;">' # s_initial # '</h3>');
							if (tablet) { WriteLine ('</th><td>'); }
						}
						
						if (s_list == ID_PROGRAMS) {
							Write('<a href="javascript:jumpto(\'program.cgi?id=' # o_object.ID() # '\');">');
						} else {
							Write('<a href="javascript:jumpto(\'sysvar.cgi?id=' # o_object.ID() # '\');">');
						}

						! Ich habe seit mindestens 15 Jahren keinen Zeilenumbruch mehr programmiert.

						s_text = o_object.Name();
						i_pointer = 0;
						i_count = 0;

						while ((i_pointer + i_length) < s_text.Length()) {
							i_count = i_count + 1;
							i_subpointer = i_pointer + i_length;
							while ((i_subpointer > i_pointer) && ((splitchar.Find (s_text.Substr (i_subpointer, 1))) < 0)) {
								i_subpointer = i_subpointer - 1;
							}
							if (i_pointer == i_subpointer) {
								i_subpointer = i_pointer + i_length;
								while (((splitchar.Find (s_text.Substr (i_subpointer, 1))) < 0) && (i_subpointer < s_text.Length())) {
									s_text = s_text.Substr (0, i_subpointer - 1) # '.' # s_text.Substr (i_subpointer + 1, s_text.Length() - i_subpointer);
								}
							}
							s_text = s_text.Substr (0, i_subpointer) # tab # s_text.Substr (i_subpointer + 1, (s_text.Length() - i_subpointer) - 1);
							i_pointer = i_subpointer;
						}
						if (s_text.Substr (s_text.Length() - 1, 1) != tab) {
							s_text = s_text # tab;
							i_count = i_count + 1;
						}

						if (s_list == ID_SYSTEM_VARIABLES) {
							i_count = 3;
							if ((o_object.ValueSubType() == istAlarm) || (o_object.ValueSubType() == istBool) ) {
								s_value = o_object.ValueName();
							}
							if (o_object.ValueSubType() == istGeneric) {
								if (o_object.ValueType() == ivtString) {  ! Bugfix ...
									o_object.ValueSubType (istChar8859);
								} else {
									s_value = o_object.Value().ToString();
									if (s_value == "") { 
										s_value = "0"; 
									}
								}
							}
							if (o_object.ValueSubType() == istEnum) {
								s_value = web.webGetValueFromList(o_object.ValueList(), o_object.Value());
							}
							if (o_object.ValueSubType() == istChar8859) {
								s_value = o_object.Value();
							}						
							if (s_value.Length() > 10) {
								s_value = s_value.Substr (0,8) # '...';
							}
							Write ('<span class="multi_4"><div onclick="this.className=\'standard active\';" class="standard button">');
						} else {
							if (i_count > 4) {
								i_count = 4;
							}
							s_value = "";
							Write ('<span class="multi_' # i_count # '"><div onclick="this.className=\'standard active\';" class="standard button">');
						}

						i_pointer = 0;
						while (i_pointer < i_count) {
							WriteXML (s_text.StrValueByIndex (tab, i_pointer));
							i_pointer = i_pointer + 1;
							if (i_pointer < i_count) {
								Write ('<br>');
							}
						}
						if (s_value != "") {
							Write ('<br><span class="gray">');
							WriteXML (s_value);
							Write ('</span>');
						}

						WriteLine ('</div></span></a>');
					}

					if (tablet) { 
						if (!b_first) {
							WriteLine ('</td></tr>');
						}
						WriteLine ('</table>'); 
					}
					
					
				}
					
			}]

			puts -nonewline $res(STDOUT)
			
			puts { </div> }
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }


		}

    }


}
