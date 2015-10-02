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

			set pin ""
			catch { import pin }
			set id ""
			set newval ""
			set timestamp ""
			set directaccess_label "";
			set directaccess_value "";
			catch { import id }
			catch { import newval }
			catch { import timestamp }
			catch { import directaccess_label };
			catch { import directaccess_value };

			array set res [rega_script {

				! PARAMATER
				object o_object = dom.GetObject("} $id {");
				var s_newval = "} $newval {";
				integer i_timestamp = "} $timestamp {";
				string s_directaccess_label = "} $directaccess_label {";
				string s_directaccess_value = "} $directaccess_value {";

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					! Variablendeklaration

					string s_temp;
					string s_temp_1;
					string s_temp_2;
					integer i_temp;
					string s_uniquename;
					object o_list;
					object o_SysVars = dom.GetObject (ID_SYSTEM_VARIABLES);

					i_temp = 0;
					s_temp_1 = "";
					s_temp_2 = "";
					while (i_temp < 10) {
						s_temp_1 = s_temp_1 # s_directaccess_value.StrValueByIndex (";", i_temp) # ";";
						s_temp_2 = s_temp_2 # s_directaccess_label.StrValueByIndex (";", i_temp) # ";";
						i_temp = i_temp + 1;
					}
					s_directaccess_value = s_temp_1;
					s_directaccess_label = s_temp_2;


					! Titel

					WriteLine ("<h1>Systemvariable</h1>");
					WriteLine ('<a href="javascript:jumpto(\'software.cgi?list=sysvar\');"><div onclick="this.className=\'active\';" class="button">zurück</div></a>');
					WriteLine ('<a href="javascript:jumpto(\'sysvar.cgi?id=' # o_object.ID() # '\');"><div onclick="this.className=\'active\';" class="button">aktualisieren</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="button">abmelden</div></a>');
					}
					WriteLine ('<a href="javascript:jumpto(\'help/sysvar.htm\');"><div class="buttonhelp">Hilfe</div></a>');

					! neue Werte eintragen wenn angegeben

					if (s_newval != "") {
						Write ('<span class="multi_2"><div class="statustrue">Neuer Wert<br>');
						WriteXML (s_newval.Substr (0,10));
						WriteLine ('</div></span>');
						if (i_timestamp != o_object.Timestamp().ToInteger()) {
							WriteLine ('<span class="multi_3"><div class="error">Wert wurde<br>inzwischen<br>geändert</div></span>');
						} else {
							o_object.State (s_newval);
						}
						if (((o_object.ValueType() == 4) && (o_object.Value() == s_newval.ToFloat())) || 
							((o_object.ValueType() == 16) && (o_object.Value() == s_newval.ToInteger())) || 
							(o_object.Value() == s_newval)) {
							WriteLine ('<span class="multi_2"><div class="success">Sollwert<br>ist erfaßt</div></span>');
						} else {
							WriteLine ('<span class="multi_3"><div class="error">Aktueller<br>Wert<br>abweichend</div></span>');
						}

						if ((s_directaccess_label != ";;;;;;;;;;") && (s_directaccess_value != ";;;;;;;;;;")) {
							s_temp = o_object.Name();
							s_temp = s_temp # " (val)\t" # s_temp # " (tag)\t";
							s_temp_1 = s_directaccess_value;
							foreach (s_temp_2, s_temp) {
								o_list = dom.GetObject (s_temp_2);
								if (!o_list) {
									if ((s_temp_1 != ";;;;;;;;;;") && (o_SysVars) && (dom.CheckName (s_temp_2, &s_uniquename, ID_SYSTEM_VARIABLES))) {
										WriteLine ('<span class="multi_4"><div>Systemvar.<br>für<br>DirectAc.<br>erstellen</div></span>');
										o_list = dom.CreateObject (OT_VARDP);
										o_list.Name (s_temp_2);
										o_SysVars.Add (o_list.ID());
										o_list.DPInfo ("");
										o_list.ValueType (ivtString);
										o_list.ValueSubType (istChar8859);
										o_list.State(s_temp_1);
									}
								} else {
									if (o_list.Value() != s_temp_1) {
										WriteLine ('<span class="multi_2"><div>DirectAc.<br>aktualis.</div></span>');
										o_list.State(s_temp_1);
									}
								}
								s_temp_1 = s_directaccess_label;
							}
						}

					}

					o_list = dom.GetObject (o_object.Name() # " (val)");
					if (o_list) {
						s_directaccess_value = o_list.Value();
					}
					o_list = dom.GetObject (o_object.Name() # " (tag)");
					if (o_list) {
						s_directaccess_label = o_list.Value();
					}

					WriteLine ('<form name="formular" method="get" action="sysvar.cgi">');

					! aktuellen Wert anzeigen
				
					if ((o_object.ValueSubType() == istAlarm) || (o_object.ValueSubType() == istBool) ) {
						s_temp = o_object.ValueName();
					}
					if (o_object.ValueSubType() == istGeneric) {
						s_temp = o_object.Value().ToString();
						if (s_temp == "") { 
							s_temp = "0"; 
						}
					}
					if (o_object.ValueSubType() == istEnum) {
						s_temp = web.webGetValueFromList(o_object.ValueList(), o_object.Value());
						if (s_directaccess_label == ";;;;;;;;;;") {
							s_directaccess_label = o_object.ValueList();
						}
					}
					if (o_object.ValueSubType() == istChar8859) {
						s_temp = o_object.Value();
					}						
					Write ('<h3>');
					WriteXML (o_object.Name());
					Write ('<br>');
					WriteXML (s_temp # ' ' # o_object.ValueUnit());
					Write (' (');
					WriteXML (o_object.Value());
					WriteLine (')</h3>');


					! Formular für neuen Wert

					WriteLine ('<script language="javascript" type="text/javascript">HiddenFormFields(["cols","counter","pin"]);</script>');
					WriteLine ('<input type="hidden" name="id" value="' # o_object.ID()  # '" />');
					WriteLine ('<input type="hidden" name="timestamp" value="' # o_object.Timestamp().ToInteger() # '" />');
					WriteLine ('<input type="hidden" name="directaccess_label" value="' # s_directaccess_label # '" />');
					WriteLine ('<input type="hidden" name="directaccess_value" value="' # s_directaccess_value # '" />');

					WriteLine ('<a href="javascript:document.formular.submit();"><div onclick="this.className=\'activeinput\';" class="inputbutton">ändern</div></a>');
					WriteLine ('<div class="inputfield"><input class="inputfield" type="input" name="newval" value="' # o_object.Value() # '" /></div>');


					! Formular für DirectAccess

					WriteLine ('<h3>DirectAccess</h3>');

					i_temp = 0;
					while (i_temp < 10) {
						WriteLine ('<p class="newline"></p>');
						WriteLine ('<div class="inputlabel">Eintrag&nbsp;' # (i_temp + 1) # '</div>');
						WriteLine ('<div class="smallinputfield">' #
							'<input class="smallinputfield" onchange="javascript:document.formular.directaccess_label.value=' #
							'update_directaccess(document.formular.directaccess_label.value,' # i_temp # ',this.value);" ' # 
							'type="input" name="da_label_' # i_temp # '" value="' # 
							s_directaccess_label.StrValueByIndex (";", i_temp) # '" /></div>');
						WriteLine ('<div class="smallinputfield">' #
							'<input class="smallinputfield" onchange="javascript:document.formular.directaccess_value.value=' #
							'update_directaccess(document.formular.directaccess_value.value,' # i_temp # ',this.value);" ' # 
							'type="input" name="da_value_' # i_temp # '" value="' # 
							s_directaccess_value.StrValueByIndex (";", i_temp) # '" /></div>');
						i_temp = i_temp + 1;
					}

					WriteLine ('</form>');


					! Rohdaten

					WriteLine ('<h3>Rohdaten</h3>');

					WriteLine ('<table>');

					WriteLine ('<tr>');
					WriteLine ('<th>Wert</th>');
					Write ('<td>');
					WriteXML (o_object.Value());
					WriteLine ('</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>Wert (Name)</th>');
					Write ('<td>');
					WriteXML (o_object.ValueName());
					WriteLine ('</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>Variable</th>');
					Write ('<td>');
					WriteXML (o_object.Variable());
					WriteLine ('</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>ID</th>');
					WriteLine ('<td>' # o_object.ID() # '</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>min</th>');
					WriteLine ('<td>' # o_object.ValueMin() # '</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>max</th>');
					WriteLine ('<td>' # o_object.ValueMax() # '</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>Einheit</th>');
					Write ('<td>');
					WriteXML (o_object.ValueUnit());
					WriteLine ('</td>');
					WriteLine ('</tr>');
					
					WriteLine ('<tr>');
					WriteLine ('<th>Werte</th>');
					Write ('<td>');
					WriteXML (o_object.ValueList());
					WriteLine ('</td>');
					WriteLine ('</tr>');
					
					WriteLine ('<tr>');
					WriteLine ('<th>Typ</th>');
					WriteLine ('<td>' # o_object.ValueType() # '</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>Untertyp</th>');
					WriteLine ('<td>' # o_object.ValueSubType() # '</td>');
					WriteLine ('</tr>');

					WriteLine ('<tr>');
					WriteLine ('<th>Timestamp</th>');
					WriteLine ('<td>' # o_object.Timestamp().Format("%d.%m.%Y %H:%M:%S") # '</td>');
					WriteLine ('</tr>');

					WriteLine ('</table>');

				}

			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010,2011 by Yellow Teddybear Software</p> }



		}


	}

}
