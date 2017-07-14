#!/bin/tclsh

# Dank an Michael Kurze für Unterstützung von HMW-IO-12-Sw14-DR.

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

				! PARAMATER

				boolean tablet = ("} $tablet {"=="1");

				string s_list = "} $list {";

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {


					string tab = '\t';

					string s_temp;
					string s_temp_idx;
					real r_temp;
					boolean b_temp;
					integer i_temp;

					string s_object_id;
					object o_object;
					object o_dp;
					string s_dp_id;
					string s_listname;
					boolean b_titlesent;

					string s_dp;
					var v_timestamp;

					string s_button_labels;
					string s_button_actions;
					string s_button_type;
					integer i_button_index;
					
					string s_button_label;
					string s_button_action;
					string s_button_unit;

					string s_list_enum = "";

					if (s_list.Substr (0,2) == 'HM') {
						Write ('<h1>');
						WriteXML (s_list);
						WriteLine ('</h1>');
						WriteLine ('<script type="text/javascript">document.title = "' # s_listname # ' - HomeMatic QuickAccess";</script>');
						WriteLine ('<a href="javascript:jumpto(\'hardware.cgi\');"><div onclick="this.className=\'standard active\';" class="standard button">zurück</div></a>');
						foreach (s_temp, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
							o_object = dom.GetObject(s_temp);
							if (o_object.HssType() == s_list) {
								foreach (s_temp, o_object.Channels().EnumUsedIDs()) {
									s_list_enum = s_list_enum # s_temp # tab;
								}
							}
						}
						s_listname = s_list;
					} else {
						s_list_enum = dom.GetObject(s_list).EnumUsedIDs();
						s_listname = dom.GetObject(s_list).Name();
						Write ('<h1>');
						WriteXML (s_listname);
						WriteLine ('</h1>');
						WriteLine ('<script type="text/javascript">document.title = "' # s_listname # ' - HomeMatic QuickAccess";</script>');
						WriteLine ('<a href="javascript:jumpto(\'index.cgi#\' + js_ianchor);"><div onclick="this.className=\'standard active\';" class="standard button">zurück</div></a>');
					}

					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="standard button">abmelden</div></a>');
					}
					WriteLine ('<a href="javascript:jumpto(\'help/channels.htm\');"><div class="standard buttonhelp">Hilfe</div></a>');
					WriteLine ("");

					if (tablet) { WriteLine ('<div class="clear"></div><table class="tablet">'); }
			
					foreach (s_object_id, s_list_enum) {
					
						o_object = dom.GetObject (s_object_id);
						
						b_titlesent = false;
						v_timestamp = false;
						
						foreach (s_dp, o_object.DPs().EnumUsedIDs() # '\tCONFIG_PENDING\tLOWBAT\tSTICKY_UNREACH\tUNREACH') {
							if (":CONFIG_PENDING:LOWBAT:STICKY_UNREACH:UNREACH:".Find (":" # s_dp # ":") != -1) {
								o_dp = dom.GetObject ("AL-" # o_object.Address().StrValueByIndex (":", 0) # ":0." # s_dp);
							} else {
								o_dp = dom.GetObject (s_dp);
							}
							
							s_button_labels = "";
							s_button_actions = "";
							s_button_type = "";
							i_button_index = 0;
							
							if ((o_dp.TypeName() == "ALARMDP") && (o_dp.Value())) {
								s_button_type = "standard warning";
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
									s_button_type = "standard error";
									s_button_labels = ".:Kommunik.<br>zur Zeit<br>gestört";
								}
							}
							
							if (o_dp.TypeName() == "HSSDP") {
					
								if (o_dp.Timestamp()) {
									if ((v_timestamp.Type() == 'boolean') || (v_timestamp < o_dp.Timestamp())) {
										v_timestamp = o_dp.Timestamp();
									}
								}
							
								! MOTION_DETECTOR
								! CLIMATECONTROL_VENT_DRIVE
								! SHUTTER_CONTACT
								! ROTARY_HANDLE_SENSOR
								! DIMMER
								! WINMATIC
								if (o_dp.HssType() == "ERROR") {
									if (o_object.HssType() == "CLIMATECONTROL_VENT_DRIVE") {
										s_button_type = 'standard error';
										s_button_labels = 'kein<br>Fehler:Ventil<br>blockiert:Ventil<br>falsch<br>montiert:Stellbereich<br>zu klein:Batterie<br>leer<br>Störpos.<br>angefahren';
									}
									if ((";MOTION_DETECTOR;ROTARY_HANDLE_SENSOR;SHUTTER_CONTACT;".Find(";" # o_object.HssType() # ";")) != -1) {
										s_button_type = 'standard error';
										s_button_labels = 'keine<br>Sabotage:.:.:.:.:.:.:Sabotage';
									}
									if (o_object.HssType() == "DIMMER") {
										s_button_type = 'standard error';
										s_button_labels = 'kein<br>Lastfehler:.:.:Lastfehler';
									}
									if (o_object.HssType() == "WINMATIC") {
										s_button_type = 'standard error';
										s_button_labels = 'Antrieb<br>OK:Fehler<br>Drehgriff:Fehler<br>Kippantrieb';
									}
									if (o_object.HssType() == "KEYMATIC") {
										s_button_type = 'standard error';
										s_button_labels = 'Antrieb<br>OK:Fehler<br>einkuppeln:Abbruch<br>Motorlauf';
									}
								} ! ERROR

								! DIMMER
								if (o_dp.HssType() == "ERROR_OVERHEAT") {
									s_button_type = "standard error";
									s_button_labels = 'Temperatur<br>OK;Überhitzung';
								} ! ERROR_OVERHEAT

								! DIMMER
								if (o_dp.HssType() == "ERROR_OVERLOAD") {
									s_button_type = "standard error";
									s_button_labels = 'keine<br>Überlast;Überlast';
								} ! ERROR_OVERLOAD
								
								! DIMMER
								if (o_dp.HssType() == "ERROR_REDUCED") {
									s_button_type = "standard error";
									s_button_labels = 'Last hoch<br>genug;Last zu<br>gering';
								} ! ERROR_REDUCED

								! POWER
								if (o_dp.HssType() == "LOWBAT") {
									s_button_type = "standard error";
									s_button_labels = 'Batterie<br>OK:Batterie<br>leer';
								}
								
								! SMOKE_DETECTOR_TEAM
								! ROTARY_HANDLE_SENSOR
								! SHUTTER_CONTACT
								! SWITCH
								if (o_dp.HssType() == "STATE") {
									if (o_object.HssType() == "WATERDETECTIONSENSOR") {
										if (o_dp.Value() < 2) {
											s_button_type = "standard warning";
										} else {
											s_button_type = "standard error";
										}
										s_button_labels = "trocken:feucht:nass";
									}
									if (o_object.HssType() == "SMOKE_DETECTOR_TEAM") {
										s_button_type = "standard error";
										s_button_labels = "kein<br>Rauch:Alarm";
									}
									if (o_object.HssType() == "SENSOR_FOR_CARBON_DIOXIDE") {
										if (o_dp.Value() < 2) {
											s_button_type = "standard warning";
										} else {
											s_button_type = "standard error";
										}
										s_button_labels = "Belastung<br>OK:Belastung<br>erhöht:Belastung<br>stark<br>erhöht";
									}
								} ! STATE

								! POWER
								if (o_dp.HssType() == "U_SOURCE_FAIL") {
									s_button_type = "standard error";
									s_button_labels = 'Betrieb<br>über<br>Netz-<br>spannung:Batterie-<br>betrieb';
								} ! U_SOURCE_FAIL

								
								! POWER
								if (o_dp.HssType() == "BAT_LEVEL") {
									s_button_labels = 'Batterie<br>' # (100 * o_dp.Value()) # '%';
								} ! BAT_LEVEL
								
								! WEATHER
								! MOTION_DETECTOR
								if (o_dp.HssType() == "BRIGHTNESS") {
									s_button_labels = "Helligkeit<br>" # o_dp.Value();
								} ! BRIGHTNESS
							
								! BLIND
								! SWITCH
								! DIMMER
								if (o_dp.HssType() == "INHIBIT") {
									s_button_type = "standard button";
									s_button_labels = 'keine<br>Tastensperre:Tastensperre';
									s_button_actions = 'true:false';
								} ! INHIBIT

								! BLIND
								! DIMMER
								! VIRTUAL_KEY
								! AKKU
								! WINMATIC
								if (o_dp.HssType() == "LEVEL") {
									if (o_object.HssType() == "WINMATIC") {
										s_button_type = "selector";
										s_button_labels = "verriegelt:zu:25%:50%:75%:auf";
										s_button_actions = "-0.05:0.00:0.25:0.50:0.75:1.00";
									}
									if (o_object.HssType() == "BLIND") {
										s_button_type = "selector";
										s_button_labels = "zu:25%:50%:75%:auf";
										s_button_actions = "0.00:0.25:0.50:0.75:1.00";
									} 
									if (o_object.HssType() == "DIMMER") {
										s_button_type = "selector";
										s_button_labels = "aus:25%:50%:75%:an";
										s_button_actions = "0.00:0.25:0.50:0.75:1.00";
									}
									if (o_object.HssType() == "VIRTUAL_KEY") {
										s_button_type = "selector";
										s_button_labels = "0%:25%:50%:75%:100%";
										s_button_actions = "0.00:0.25:0.50:0.75:1.00";
									}
									if (o_object.HssType() == "AKKU") {
										s_button_labels = "Batterie<br>" # (o_dp.Value() * 100).ToInteger() # "%";
									}
								}
								
								! MOTION_DETECTOR
								if (o_dp.HssType() == "MOTION") {
									s_button_type = "standard status";
									s_button_labels = 'keine<br>Bewegung:Bewegung<br>erkannt';
								} ! MOTION

								! KEYMATIC
								if (o_dp.HssType() == "OPEN") {
									s_button_type = "standard button";
									s_button_labels = "öffnen";
									s_button_actions = "true";
								} ! OPEN

								! SWITCH_INTERFACE
								if (o_dp.HssType() == "PRESS") {
									s_button_type = "standard button";
									s_button_labels = "Tastendruck";
									s_button_actions = "true";
								} ! PRESS

								! KEY
								! CENTRAL_KEY
								! VIRTUAL_KEY
								if (o_dp.HssType() == "PRESS_LONG") {
									s_button_type = "standard button";
									s_button_labels = "langer<br>Tastendruck";
									s_button_actions = "true";
								} ! PRESS_LONG
								
								! KEY
								! CENTRAL_KEY
								! VIRTUAL_KEY
								if (o_dp.HssType() == "PRESS_SHORT") {
									s_button_type = "standard button";
									s_button_labels = "kurzer<br>Tastendruck";
									s_button_actions = "true";
								} ! PRESS_SHORT
								
								! WEATHER
								if (o_dp.HssType() == "RAINING") {
									s_button_type = "info";
									s_button_labels = 'kein<br>Regen:Regen';
								}

								! SENSOR
								if (o_dp.HssType() == "SENSOR") {
									s_button_type = "info";
									s_button_labels = "zu:offen";
								} ! SENSOR

								! PULSE_SENSOR
								if (o_dp.HssType() == "SEQUENCE_OK") {
									s_button_type = "standard button";
									s_button_labels = "auslösen";
									s_button_actions = "true";
								} ! SEQUENCE_OK

								! CLIMATECONTROL_REGULATOR
								! CLIMATECONTROL_RT_TRANSCEIVER
								if ((";SETPOINT;SET_TEMPERATURE;".Find (";" # o_dp.HssType() # ";")) != -1) {
									s_button_type = "selector";
									if ((o_dp.Value() > 0) && (o_dp.Value() < 99)) {
										foreach (s_temp, '-4\t-2\t-1\t-0.5\t0\t0.5\t1\t2\t4') {
											r_temp = o_dp.Value() + s_temp.ToFloat();
											if ((r_temp > 15) && (r_temp < 25)) {
												s_button_actions = s_button_actions # r_temp.ToString(1) # ':';
												s_button_labels = s_button_labels # r_temp.ToString(1) # '°C:';
											}
										}
									} else {
										r_temp = 17.0;
										while (r_temp < 22.0) {
											r_temp = r_temp + 1.0;
											s_button_actions = s_button_actions # r_temp.ToString(1) # ':';
											s_button_labels = s_button_labels # r_temp.ToString(1) # '°C:';
										}
									}
									s_button_actions = s_button_actions # '0.0:99.0:';
									s_button_labels = s_button_labels # 'aus:Ventil<br>öffnen:';
								} ! SETPOINT

								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "CONTROL_MODE") {
									s_button_type = "info";
									s_button_labels = "Auto:Manu:Party:Boost";
								}
								
								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "FAULT_REPORTING") {
									s_button_type = "info";
									s_button_labels = "kein<br>Fehler:Ventil<br>blockiert:Stellbereich<br>zu<br>groß:Stellbereich<br>zu<br>klein:Kommunik.<br>gestört::Batterie<br>leer:Störpos.<br>angefahren";
								}
								
								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "BATTERY_STATE") {
									s_button_unit = o_dp.ValueUnit();
									s_button_labels = "Batt.<br>" # o_dp.Value().ToString(1) # s_button_unit;
								}

								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "BOOST_STATE") {
									s_button_unit = o_dp.ValueUnit();
									s_button_labels = "Boost<br>" # o_dp.Value().ToString(1) # s_button_unit;
								}

								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "AUTO_MODE") {
									s_button_type = "standard button";
									s_button_labels = "Auto";
									s_button_actions = "true";
								}

								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "MANU_MODE") {
									s_button_type = "standard button";
									s_button_labels = "Manueller<br>Modus<br>(19&nbsp;°C)";
									s_button_actions = "19.0";
								}

								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "BOOST_MODE") {
									s_button_type = "standard button";
									s_button_labels = "Boost";
									s_button_actions = "true";
								}

								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "COMFORT_MODE") {
									s_button_type = "standard button";
									s_button_labels = "Komfort-<br>Temperatur";
									s_button_actions = "true";
								}

								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "LOWERING_MODE") {
									s_button_type = "standard button";
									s_button_labels = "Absenk-<br>Temperatur";
									s_button_actions = "true";
								}

								! SMOKE_DETECTOR_TEAM
								! ROTARY_HANDLE_SENSOR
								! SHUTTER_CONTACT
								! SWITCH
								! INPUT_OUTPUT
								! DIGITAL_OUTPUT
								! DIGITAL_INPUT
								if (o_dp.HssType() == "STATE") {
									if ((":SHUTTER_CONTACT:DIGITAL_INPUT:".Find (":" # o_object.HssType() # ":")) != -1) {
										s_button_type = "info";
										s_button_labels = "zu:offen";
									}
									if (o_object.HssType() == "ROTARY_HANDLE_SENSOR") {
										s_button_type = "info";
										s_button_labels = "zu:gekippt:offen";
									}
									if (o_object.HssType() == "TILT_SENSOR") {
										s_button_type = "info";
										s_button_labels = "aufrecht:gekippt";
									}
									if ((":ALARMACTUAOR:SWITCH:SIGNAL_LED:SIGNAL_CHIME:INPUT_OUTPUT:DIGITAL_OUTPUT:".Find (":" # o_object.HssType() # ":")) != -1) {
										s_button_type = "standard button";
										s_button_labels = "aus:ein";
										s_button_actions = "true:false";
									}
									if (o_object.HssType() == "KEYMATIC") {
										s_button_type = "standard button";
										s_button_labels = "verriegelt:entriegelt";
										s_button_actions = "true:false";
									}										
								} ! STATE

								! DIGITAL_ANALOG_INPUT
								if (o_object.HssType() == "DIGITAL_ANALOG_INPUT") {
									if (o_dp.Value("BEHAVIOUR") == 0) {
										s_button_labels = o_dp.Value().ToString(1);
									} else {
										s_button_type = "info";
										s_button_labels = "aus:ein";
									}
								}
							
								! WINMATIC
								if (o_dp.HssType() == "STATE_UNCERTAIN") {;
									s_button_type = "standard status";
									s_button_labels = 'Zustand<br>OK:Zustand<br>unbekannt';
								} ! STATE_UNCERTAIN

								! AKKU
								if (o_dp.HssType() == "STATUS") {
									s_button_type = "info";
									s_button_labels = 'Erhaltungsladung:Laden:Akkubetrieb:Status<br>unbekannt';
								} ! STATUS

								! BLIND
								! WINMATIC
								if (o_dp.HssType() == "STOP") {
									s_button_type = "standard button";
									s_button_labels = "Stop";
									s_button_actions = "true";
								} ! STOP

								! WEATHER
								! CLIMATECONTROL_RT_TRANSCEIVER
								if ((";TEMPERATURE;HUMIDITY;WIND_SPEED;AIR_PRESSURE;ACTUAL_TEMPERATURE;".Find (";" # o_dp.HssType() # ";")) != -1) {
									if (o_dp.ValueUnit() == "Â°C") {
										s_button_unit = "&nbsp;°C";
									} else {
										s_button_unit = o_dp.ValueUnit();
									}
									s_button_labels = o_dp.Value().ToString(1) # s_button_unit;
								}
								
								! WEATHER
								if (o_dp.HssType() == "WIND_DIRECTION_RANGE") {
									s_button_unit = "&nbsp;°";
									s_button_labels = "Schwankung<br>Wind<br>" # o_dp.Value().ToString(0) # s_button_unit;
								}
									
									
								! WEATHER
								if (o_dp.HssType() == "WIND_DIRECTION") {
									s_button_labels = "Nord:Nord-Ost:Ost:Süd-Ost:Süd:Süd-West:West:Nord-West:Nord".StrValueByIndex(":",   ((23+o_dp.Value())/45));
								}
									
								! POWERMETER
								if ((";ENERGY_COUNTER;POWER;CURRENT;VOLTAGE;FREQUENCY;".Find (";" # o_dp.HssType() # ";")) != -1) {
									s_button_unit = o_dp.ValueUnit();
									s_button_labels = o_dp.Value().ToString(1) # s_button_unit;
								}

								! POWER
								if (o_dp.HssType() == "U_USBD_OK") {
									s_button_type = "standard status";
									s_button_labels = 'USB<br>inaktiv:USB<br>aktiv';
								} ! U_USBD_OK

								! CLIMATECONTROL_VENT_DRIVE
								! CLIMATECONTROL_RT_TRANSCEIVER
								if (o_dp.HssType() == "VALVE_STATE") {
									s_button_labels = o_dp.Value() # "%";
								} ! VALVE_STATE
							
								! BLIND
								! SWITCH
								! DIMMER
								if (o_dp.HssType() == "WORKING") {
									if (o_object.HssType() == "BLIND") {
										s_button_type = "standard status";
										s_button_labels = 'nicht in<br>Bewegung:in<br>Bewegung';
									}
									if ((":SWITCH:SIGNAL_LED:SIGNAL_CHIME:ALARMACTUATOR:".Find (":" # o_object.HssType() # ":")) != -1) {
										s_button_type = "standard status";
										s_button_labels = 'Schaltdauer<br>inaktiv:Schaltdauer<br>aktiv';
									}
									if (o_object.HssType() == "DIMMER") {
										s_button_type = "standard status";
										s_button_labels = 'Einstellung<br>fixiert:Einstellung<br>wird<br>geändert';
									}
								} ! WORKING

						
							} ! TypeName=HSSDP
							
							! TITEL ANZEIGEN
							if ((!b_titlesent) && (s_button_labels != "")) {
								b_titlesent = true;
								if (tablet) { WriteLine ('<tr><th>'); }

								Write ('<div class="clear"></div><a name="');
								WriteXML (o_object.ID());
								WriteLine ('"></a><h3><table class="blind"><td class="wide">');
								i_temp = o_object.Name().Find(s_listname);
								if (i_temp >= 0) {
									s_temp = o_object.Name().Substr (0, i_temp) # '-' # o_object.Name().Substr(i_temp + s_listname.Length(), o_object.Name().Length() - i_temp);
									i_temp = s_temp.Find('-.');
									if (i_temp == 0) {
										s_temp = s_temp.Substr (2, s_temp.Length() - 2);
									}
									WriteXML (s_temp);
								} else {
									WriteXML (o_object.Name());
								}
								WriteLine ('</td><td><div class="toparrow" onclick="jumptotop();"></div></td></table></h3>')

								if (tablet) { WriteLine ('</th><td>'); }
							}
							
							! BUTTONS ANZEIGEN
							i_button_index = 0;
							r_temp = o_dp.Value();
							if (r_temp < 0) {
								r_temp = -0.05;
							} else {
								r_temp = 0.25 * (4.0 * (0.12 + r_temp)).ToInteger();
							}
							while (s_button_labels.StrValueByIndex (":", i_button_index) != "") {
								s_button_label = s_button_labels.StrValueByIndex (":", i_button_index);
								s_button_action = s_button_actions.StrValueByIndex (":", i_button_index);
								if ((s_button_type == "selector") || (s_button_type == "") ||
									((s_button_type == "standard button") && (s_button_action != o_dp.Value())) ||
									((s_button_type == "standard status") || (s_button_type == "info") || (s_button_type == "standard error") || (s_button_type == "standard warning")) && (i_button_index == o_dp.Value().ToInteger())) {
									i_temp = 1;
									while (s_button_label.StrValueByIndex ('<', i_temp) != "") {
										i_temp = i_temp + 1;
									}
									if ((s_button_type == "standard button") || (s_button_type == "selector")) {
										Write ('<a href="javascript:jumpto(\'action.cgi?list=' # s_list # '&anchor=' # o_object.ID() # '&id=' # o_dp.ID() # '&action=' # s_button_action # '\');">');
									}
									Write ('<span class="multi_' # i_temp # '">');
									if ((s_button_type == "info") || (s_button_type == "")) {
										Write ('<div class="standard">');
									}
									if ((s_button_type == "standard error") || (s_button_type == "standard status") || (s_button_type == "standard warning")) {
										Write ('<div class="' # s_button_type # i_button_index # '">');
									}
									if (s_button_type == "standard button") {
										Write ('<div onclick="this.className=\'standard active\';" class="standard button' # o_dp.Value() # '">');
									}
									if (s_button_type == "selector") {
										Write ('<div onclick="this.className=\'standard active\';" class="standard button' # (r_temp == s_button_action.ToFloat()) # '">');
									}
									Write (s_button_label # '</div></span>');
									if ((s_button_type == "standard button") || (s_button_type == "selector")) {
										Write ('</a>');
									}
									WriteLine ("");
								}
								i_button_index = i_button_index + 1;
							}
						}

						if (b_titlesent) {
							if (tablet) { WriteLine ('</td><td>'); }
							! TIMESTAMP
							if (v_timestamp.Type() == 'time') {
								WriteLine ('<span class="multi_2"><div class="standard timestamp">' # v_timestamp.Format("%d.%m.%Y<br />%H:%M:%S") # '</div></span>');
							}
							if (tablet) { WriteLine ('</td></tr>'); }
						}

					}	
					
				if (tablet) { WriteLine ('</table>'); }
				
				}
				
			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { </div> }
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }

		}
    }
}