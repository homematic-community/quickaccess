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
			puts { <link href="style.css" rel="stylesheet" type="text/css" /> }
			puts { <meta name="viewport" content="width=device-width, initial-zoom=1" /> }
		}

		cgi_body {

			puts { <script src="style.js" type="text/javascript"></script> }

			set pin ""
			catch { import pin }
			set id ""
			catch { import id }
			set confirm ""
			catch { import confirm }
			set list ""
			catch { import list }

			array set res [rega_script {

				! PARAMETER/PIN

				string s_id = "} $id {";
				boolean b_all = "} $list {"=="all";
				boolean b_confirm = "} $confirm {"=="true";
				
				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					! VARIABLE
				
					integer i_temp;
					boolean b_visible;

					object o_object;
					object o_dp;
					string s_dp;

					string s_button_labels;
					string s_button_type;
					string s_button_label;
					
					string s_anchor = "top";

					object o_confirmed = dom.GetObject ("QuickAccess Servicemeldungen bestaetigt");
					string s_confirmed = o_confirmed.Value();
					if ((s_id != '') && (dom.GetObject (s_id))) {
						i_temp = s_confirmed.Find (':' # s_id # ':');
						if ((b_confirm) && (i_temp < 0)) {
							s_confirmed = s_confirmed # s_id # ':';
						}
						if ((!b_confirm) && (i_temp >= 0)) {
							s_confirmed = s_confirmed.Substr (0, i_temp) # s_confirmed.Substr (i_temp + s_id.Length() + 1, s_confirmed.Length() - s_id.Length() - i_temp);
						}
						o_confirmed.State (s_confirmed);
					}
					WriteLine ("<h1>Service&shy;meldungen</h1>");
					WriteLine ('<a href="javascript:jumpto(\'index.cgi#\' + js_ianchor);"><div onclick="this.className=\'active\';" class="button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div onclick="this.className=\'active\';" class="button">abmelden</div></a>');
					}
					WriteLine ('<span class="multi_4"><div><span id="errors_count">offene<br>Meldungen<br>werden<br>gesucht</span></div></span>');
					WriteLine ('<a href="javascript:jumpto(\'errors.cgi?list=' # ("all:errors".StrValueByIndex (":", b_all)) # '\');"><span class="multi_3"><div onclick="this.className=\'active\';" class="button' # b_all # '">' # ('alle:nur offene'.StrValueByIndex (':', b_all)) # '<br>Meldungen<br>anzeigen</div></span></a>');
						
					WriteLine ('<a href="javascript:jumpto(\'help/errors.htm\');"><div class="buttonhelp">Hilfe</div></a>');
					WriteLine ("");

					foreach (s_dp, dom.GetObject("QuickAccess Servicemeldungen").Value()) {
						o_object = dom.GetObject (s_dp.StrValueByIndex (":", 0));
						if (o_object) {
							s_dp = s_dp.StrValueByIndex (":", 1);
							o_dp = dom.GetObject (s_dp);
							if ((s_confirmed.Find (':' # s_dp # ':') < 0) || (b_all)) {
								
								s_button_labels = "";
								s_button_type = "";
								
								WriteLine ('<!-- ' # s_dp # ' / ' # o_dp.Name() # ' / ' # o_dp.Value() # ' / ' # o_dp.HssType() # ' / ' # o_dp.TypeName() # ' -->');
								
								if ((o_dp.TypeName() == "ALARMDP") && (o_dp.Value())) {
									s_button_type = "warning";
									s_dp = o_dp.Name().StrValueByIndex(".", 1);
									if (s_dp == "CONFIG_PENDING") {
										s_button_labels = ".:Konfigur.-<br>daten<br>übertragen";
									}
									if (s_dp == "LOWBAT") {
										s_button_labels = ".:Batterie-<br>stand<br>niedrig";
									}
									if (s_dp == "STICKY_UNREACH") {
										s_button_labels = ".:Kommunik.<br>war<br>gestört";
									}
									if (s_dp == "UNREACH") {
										s_button_type = "error";
										s_button_labels = ".:Kommunik.<br>zur Zeit<br>gestört";
									}
								}
								
								if (o_dp.TypeName() == "HSSDP") {

									o_object = dom.GetObject(o_dp.Device());
									
									! MOTION_DETECTOR
									! CLIMATECONTROL_VENT_DRIVE
									! SHUTTER_CONTACT
									! ROTARY_HANDLE_SENSOR
									! DIMMER
									! WINMATIC
									if (o_dp.HssType() == "ERROR") {
										if (o_object.HssType() == "CLIMATECONTROL_VENT_DRIVE") {
											s_button_type = 'error';
											s_button_labels = 'kein<br>Fehler:Ventil<br>blockiert:Ventil<br>falsch<br>montiert:Stellbereich<br>zu klein:Batterie<br>leer<br>Störpos.<br>angefahren';
										}
										if ((";MOTION_DETECTOR;ROTARY_HANDLE_SENSOR;SHUTTER_CONTACT;".Find(";" # o_object.HssType() # ";")) != -1) {
											s_button_type = 'error';
											s_button_labels = 'keine<br>Sabotage:.:.:.:.:.:.:Sabotage';
										}
										if (o_object.HssType() == "DIMMER") {
											s_button_type = 'error';
											s_button_labels = 'kein<br>Lastfehler:.:.:Lastfehler';
										}
										if (o_object.HssType() == "WINMATIC") {
											s_button_type = 'error';
											s_button_labels = 'Antrieb<br>OK:Fehler<br>Drehgriff:Fehler<br>Kippantrieb';
										}
										if (o_object.HssType() == "KEYMATIC") {
											s_button_type = 'error';
											s_button_labels = 'Antrieb<br>OK:Fehler<br>einkuppeln:Abbruch<br>Motorlauf';
										}
									} ! ERROR

									! DIMMER
									if (o_dp.HssType() == "ERROR_OVERHEAT") {
										s_button_type = "error";
										s_button_labels = 'Temperatur<br>OK;Überhitzung';
									} ! ERROR_OVERHEAT

									! DIMMER
									if (o_dp.HssType() == "ERROR_OVERLOAD") {
										s_button_type = "error";
										s_button_labels = 'keine<br>Überlast;Überlast';
									} ! ERROR_OVERLOAD
									
									! DIMMER
									if (o_dp.HssType() == "ERROR_REDUCED") {
										s_button_type = "error";
										s_button_labels = 'Last hoch<br>genug;Last zu<br>gering';
									} ! ERROR_REDUCED

									! POWER
									if (o_dp.HssType() == "LOWBAT") {
										s_button_type = "error";
										s_button_labels = 'Batterie<br>OK:Batterie<br>leer';
									}
									
									! SMOKE_DETECTOR_TEAM
									! ROTARY_HANDLE_SENSOR
									! SHUTTER_CONTACT
									if (o_dp.HssType() == "STATE") {
										if (o_object.HssType() == "WATERDETECTIONSENSOR") {
											if (o_dp.Value() < 2) {
												s_button_type = "warning";
											} else {
												s_button_type = "error";
											}
											s_button_labels = "trocken:feucht:nass";
										}
										if (o_object.HssType() == "SMOKE_DETECTOR_TEAM") {
											s_button_type = "error";
											s_button_labels = "kein<br>Rauch:Alarm";
										}
										if (o_object.HssType() == "SENSOR_FOR_CARBON_DIOXIDE") {
											if (o_dp.Value() < 2) {
												s_button_type = "warning";
											} else {
												s_button_type = "error";
											}
											s_button_labels = "Belastung<br>OK:Belastung<br>erhöht:Belastung<br>stark<br>erhöht";
										}
									} ! STATE

									! POWER
									if (o_dp.HssType() == "U_SOURCE_FAIL") {
										s_button_type = "error";
										s_button_labels = 'Betrieb<br>über<br>Netz-<br>spannung:Batterie-<br>betrieb';
									} ! U_SOURCE_FAIL

								} ! HSSDP
								
								! BUTTONS ANZEIGEN
								if (o_dp.Value() > 0) {
									s_button_label = s_button_labels.StrValueByIndex (":", o_dp.Value());
									i_temp = 1;
									while (s_button_label.StrValueByIndex ('<', i_temp) != "") {
										i_temp = i_temp + 1;
									}
									WriteLine ('');
									Write ('<a name="' # o_dp.ID() # '"><h3>');
									WriteXML (o_object.Name());
									WriteLine ('</h3></a>');
									b_visible = (s_confirmed.Find (':' # o_dp.ID() # ':') >= 0);
									WriteLine ('<a href="javascript:jumpto(\'errors.cgi?id=' # o_dp.ID() # '&confirm=' # (!b_visible) # '#' # s_anchor # '\');"><div onclick="this.className=\'active\';" class="button' # b_visible # '">' # ("ausblenden:einblenden".StrValueByIndex (":", b_visible)) # '</div></a>');
									WriteLine ('<span class="multi_' # i_temp # '"><div class="' # s_button_type # o_dp.Value() # '">' # s_button_label # '</div></span>');
									s_anchor = o_dp.ID();
								}
							}
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
