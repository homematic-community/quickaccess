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

			set list ""
			catch { import list }
			set pin ""
			catch { import pin }
	
			array set res [rega_script {

				! PARAMETER
				string s_list = "} $list {";

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
						s_list = ID_PROGRAMS;
					}
					if (s_list == 'sysvar') {
						WriteLine ('<h1>Systemvariable</h1>');
						s_list = ID_SYSTEM_VARIABLES;
					}
						
					WriteLine ('<a href="javascript:jumpto(\'index.cgi#0\');"><div onclick="this.className=\'active\';" class="button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="button">abmelden</div></a>');
					}
					WriteLine ('<a href="javascript:jumpto(\'help/software.htm\');"><div class="buttonhelp">Hilfe</div></a>');
					WriteLine ('<h3></h3>');

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
		
					foreach (s_object_id, dom.GetObject(s_list).EnumUsedIDs()) {
						o_object = dom.GetObject (s_object_id);
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
							Write ('<span class="multi_4"><div onclick="this.className=\'active\';" class="button">');
						} else {
							if (i_count > 4) {
								i_count = 4;
							}
							s_value = "";
							Write ('<span class="multi_' # i_count # '"><div onclick="this.className=\'active\';" class="button">');
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

				}
					
			}]

			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2014 by Yellow Teddybear Software</p> }


		}

    }


}
