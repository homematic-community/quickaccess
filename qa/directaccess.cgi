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
			set newvalue ""
			catch { import id }
			catch { import newvalue }
			set pin ""
			catch { import pin }
	
			array set res [rega_script {

				! PARAMETER
				integer i_id = "} $id {".ToInteger();
				string s_newvalue = "} $newvalue {";

			
				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					string s_idx;
					object o_labels;
					object o_values;
					object o_object;
					string s_labels;
					string s_values;
					string s_label;
					string s_value;
					integer i_temp;
					boolean b_temp;

					string tab = "\t";
					string splitchar=" .,-/_";
					integer i_length = 11;
					integer i_pointer;
					integer i_subpointer;
					integer i_count;
					string s_text;
					
					string s_programs;
					object o_program;
					string s_list_enum = "";

					WriteLine ('<h1>DirectAccess</h1>');
					WriteLine ('<a href="javascript:jumpto(\'index.cgi#0\');"><div onclick="this.className=\'active\';" class="button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="button">abmelden</div></a>');
					}
					WriteLine ('<span class="multi_4"><div><span id="errors_count">offene<br>Meldungen<br>werden<br>gesucht</span></div></span>');
					WriteLine ('<a href="javascript:jumpto(\'help/directaccess.htm\');"><div class="buttonhelp">Hilfe</div></a>');

					if ((i_id != 0) && (s_newvalue != '')) {
						o_object = dom.GetObject (i_id);
						if (o_object) {
							if (o_object.IsTypeOf (OT_VARDP)) {
								WriteLine ('<span class="multi_2"><div>Wert<br>setzen</div></span>');
								o_object.State(s_newvalue);
							} else {
								WriteLine ('<span class="multi_2"><div>Programm<br>starten</div></span>');
								o_object.ProgramExecute();
							}
						}
					}

					o_object = dom.GetObject ('QuickAccess DirectAccess');
					if (o_object) {
						s_programs = o_object.Value();
						if (s_programs != ':') {
							WriteLine ('<h3>Programme</h3>');
							foreach (s_idx, s_programs.Split(':')) {
								o_program = dom.GetObject (s_idx);
								if (o_program) {
									s_list_enum = s_list_enum # o_program.Name() # tab;
								}
							}
						}
					}
				
					foreach (s_idx, s_list_enum # dom.GetObject (ID_SYSTEM_VARIABLES).EnumUsedNames()) {
						s_labels = ";;;;;;;;;;";
						s_values = ";;;;;;;;;;";
						o_object = dom.GetObject (s_idx);
						if (o_object.IsTypeOf (OT_VARDP)) {
							o_labels = dom.GetObject (s_idx # " (tag)");
							o_values = dom.GetObject (s_idx # " (val)");
							if ((o_labels) && (o_values)) {
								s_labels = o_labels.Value();
								s_values = o_values.Value();
							}
						} else {
							s_labels = o_object.Name() # ";;;;;;;;;;";
							s_values = "true;;;;;;;;;";
						}
						if ((s_labels != ";;;;;;;;;;") && (s_values != ";;;;;;;;;;")) {

							if (!o_object.IsTypeOf (786433)) {
								Write ('<h3><a name="' # o_object.ID() # '">');
								WriteXML (s_idx);
								WriteLine ('</a></h3>');
							}
							
							i_temp = 0;
							while (i_temp < 10) {
								s_label = s_labels.StrValueByIndex (";", i_temp);
								s_value = s_values.StrValueByIndex (";", i_temp);
								if ((s_label != "") && (s_value != "")) {
									b_temp = (((o_object.ValueType() == 4) && (o_object.Value() == s_value.ToFloat())) || 
										((o_object.ValueType() == 16) && (o_object.Value() == s_value.ToInteger())) || 
										(o_object.Value().ToString() == s_value));

									s_text = s_label;
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

									if (i_count > 4) {
										i_count = 4;
									}

									Write ('<a href="javascript:jumpto(\'directaccess.cgi?id=' # o_object.ID() # '&newvalue=' # s_value # '#' # o_object.ID() # '\');">');
									Write ('<span class="multi_' # i_count # '">');
									Write ('<div onclick="this.className=\'active\';" class="button' # b_temp # '">');
							
									i_pointer = 0;
									while (i_pointer < i_count) {
										WriteXML (s_text.StrValueByIndex (tab, i_pointer));
										i_pointer = i_pointer + 1;
										if (i_pointer < i_count) {
											Write ('<br>');
										}
									}
									WriteLine ('</div></span></a>');

								}

								i_temp = i_temp + 1;
							}
							WriteLine ('');
						}
					}

				}
					
			}]

			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2014 by Yellow Teddybear Software</p> }

			puts { <script src="errors-js.cgi" type="text/javascript"></script> }

		}

    }


}
