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
    		cgi_title "DirectAccess - HomeMatic QuickAccess"
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
			set newvalue ""
			catch { import id }
			catch { import newvalue }
			set pin ""
			catch { import pin }
			set tablet ""
			catch { import tablet }
	
			array set res [rega_script {

				! PARAMETER
				integer i_id = "} $id {".ToInteger();
				string s_newvalue = "} $newvalue {";
				boolean tablet = ("} $tablet {"=="1");
			
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
					WriteLine ('<a href="javascript:jumpto(\'index.cgi#0\');"><div onclick="this.className=\'standard active\';" class="standard button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="standard button">abmelden</div></a>');
					}
					WriteLine ('<span class="multi_4"><div class="standard"><span id="errors_count">offene<br>Meldungen<br>werden<br>gesucht</span></div></span>');
					WriteLine ('<a href="javascript:jumpto(\'help/directaccess.htm\');"><div class="standard buttonhelp">Hilfe</div></a>');

					if ((i_id != 0) && (s_newvalue != '')) {
						o_object = dom.GetObject (i_id);
						if (o_object) {
							if (o_object.IsTypeOf (OT_VARDP)) {
								WriteLine ('<span class="multi_2"><div class="standard">Wert<br>setzen</div></span>');
								o_object.State(s_newvalue);
							} else {
								WriteLine ('<span class="multi_2"><div class="standard">Programm<br>starten</div></span>');
								o_object.ProgramExecute();
							}
						}
					}

					if (tablet) { WriteLine ('<div class="clear"></div><table class="tablet">'); }

					o_object = dom.GetObject ('QuickAccess DirectAccess');
					if (o_object) {
						s_programs = o_object.Value();
						if (s_programs != ':') {
							if (tablet) { WriteLine ('<tr><th>'); }
							WriteLine ('<div class="clear"></div><h3><table class="blind"><td class="wide">Programme</td><td><div class="toparrow" onclick="jumptotop();"></div></td></table></h3>');
							if (tablet) { WriteLine ('</th><td>'); }
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
								if (tablet) { WriteLine ('<tr><th>'); }
								Write ('<div class="clear"></div><a name="' # o_object.ID() # '"></a><h3><table class="blind"><td class="wide">');
								WriteXML (s_idx);
								WriteLine ('</td><td><div class="toparrow" onclick="jumptotop();"></div></td></table></h3>');
								if (tablet) { WriteLine ('</th><td>'); }
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
									Write ('<div onclick="this.className=\'standard active\';" class="standard button' # b_temp # '">');
							
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
							if (!o_object.IsTypeOf (786433) && tablet) { WriteLine ('</td></tr>'); }
						}
					}

					if (tablet) { WriteLine ('</table>'); }

				}
					
			}]

			puts -nonewline $res(STDOUT)
			
			puts { </div> }
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }

			puts { <script async src="errors-js.cgi" type="text/javascript"></script> }

		}

    }


}
