#!/bin/tclsh

load tclrega.so
source [file join $env(DOCUMENT_ROOT) once.tcl]
source [file join $env(DOCUMENT_ROOT) cgi.tcl]

set _cgi(debug) -on

cgi_eval {
	

	cgi_input
	cgi_content_type "text/javascript; charset=iso-8859-1"
	cgi_http_head

	array set res [rega_script {
	
		! VARIABLE

		string tab = '\t';
		object o_object;
		string s_object_id;
		object o_dp;
		string s_dp_id;
		string s_list_enum;
		string s_appendix;

		string s_dp;
		string s_confirmed_new = ':';
		string s_errors_new;
		boolean b_confirmed;
		
		! SYSTEMVARIABLE ERSTELLEN

		real i_diff;

		string s_uniquename;
		object o_sysvars;
		foreach (s_appendix, '' # tab # ' bestaetigt' # tab # ' Zaehler') {
			o_sysvars = dom.GetObject (ID_SYSTEM_VARIABLES);
			o_object = dom.GetObject ('QuickAccess Servicemeldungen' # s_appendix);
			if (!o_object) {
				if ((o_sysvars) && (dom.CheckName ('QuickAccess Servicemeldungen' # s_appendix, &s_uniquename, ID_SYSTEM_VARIABLES))) {
					o_object = dom.CreateObject (OT_VARDP);
					o_object.Name ('QuickAccess Servicemeldungen' # s_appendix);
					o_sysvars.Add (o_object.ID());
					o_object.DPInfo ("");
					o_object.ValueType (ivtString);
					o_object.ValueSubType (istChar8859);
					o_object.State("");
				}
			}
			if (s_appendix == '') {
				object o_errors = o_object;
				if (o_errors.Value() == '') {
					i_diff = 60;
				} else {
					i_diff = (system.Date("%Y-%m-%d %H:%M:%S").ToTime() - o_errors.Timestamp()).ToInteger();
				}
			}
			if (s_appendix == ' bestaetigt') {
				object o_confirmed = o_object;
			}
			if (s_appendix == ' Zaehler') {
				object o_counter = o_object;
			}
		}

		! SYSTEMVARIABLE AUSLESEN
		string s_errors_old = o_errors.Value();
		string s_confirmed_old = o_confirmed.Value();
		string s_counter = o_counter.Value();
		
		if (i_diff < 60) {
			integer i_errors_batt = s_counter.StrValueByIndex (':', 0);
			integer i_errors_comm = s_counter.StrValueByIndex (':', 1);
			integer i_errors_conf = s_counter.StrValueByIndex (':', 2);
			integer i_errors_misc = s_counter.StrValueByIndex (':', 3);
			s_errors_new = s_errors_old;
		} else {
			integer i_errors_comm = 0;
			integer i_errors_batt = 0;
			integer i_errors_conf = 0;
			integer i_errors_misc = 0;
			o_errors.State (s_errors_old); ! timestamp aktualisieren um Doppelaufruf zu verhindern
			s_errors_new = '';
			
			foreach (s_object_id, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
			
				o_object = dom.GetObject (s_object_id);
			
				s_list_enum = "";
				foreach (s_dp, 'CONFIG_PENDING\tLOWBAT\tSTICKY_UNREACH\tUNREACH') {
					o_dp = dom.GetObject ("AL-" # o_object.Address().StrValueByIndex (":", 0) # ":0." # s_dp);
					if (o_dp) {
						s_list_enum = s_list_enum # o_dp.ID() # tab;
					}
				}
				
				foreach (s_dp, o_object.Channels().EnumUsedIDs()) {
					s_list_enum = s_list_enum # dom.GetObject(s_dp).DPs().EnumUsedIDs() # tab;
				}
				
				foreach (s_dp, s_list_enum) {
					o_dp = dom.GetObject (s_dp);
					b_confirmed = (s_confirmed_old.Find (':' # s_dp # ':') >= 0);
					
					if ((o_dp.TypeName() == "ALARMDP") && (o_dp.Value())) {
						s_errors_new = s_errors_new # o_object.ID() # ":" # s_dp # tab;
						if (b_confirmed) {
							s_confirmed_new = s_confirmed_new # s_dp # ':';
						} else {
							s_dp = o_dp.Name().StrValueByIndex (".", 1);
							if (s_dp == "CONFIG_PENDING") {
								i_errors_conf = i_errors_conf + 1;
							} else {
								if (s_dp == "LOWBAT") {
									i_errors_batt = i_errors_batt + 1;
								} else {
									if ((s_dp == "STICKY_UNREACH") || (s_dp == "UNREACH")) {
										i_errors_comm = i_errors_comm + 1;
									} else {
										i_errors_misc = i_errors_misc + 1;
									}
								}
							}
						}
					}
					
					if ((o_dp.TypeName() == "HSSDP") && (o_dp.Value() != 0)) {

						if (b_confirmed) {
							s_confirmed_new = s_confirmed_new # s_dp # ':';
						}

						o_object = dom.GetObject(o_dp.Device());
						
						! MOTION_DETECTOR
						! CLIMATECONTROL_VENT_DRIVE
						! SHUTTER_CONTACT
						! ROTARY_HANDLE_SENSOR
						! DIMMER
						! WINMATIC
						if (o_dp.HssType() == "ERROR") {								
							i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
							s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
						} ! ERROR

						! DIMMER
						if (o_dp.HssType() == "ERROR_OVERHEAT") {
							i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
							s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
						} ! ERROR_OVERHEAT

						! DIMMER
						if (o_dp.HssType() == "ERROR_OVERLOAD") {
							i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
							s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
						} ! ERROR_OVERLOAD
						
						! DIMMER
						if (o_dp.HssType() == "ERROR_REDUCED") {
							i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
							s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
						} ! ERROR_REDUCED

						! POWER
						if (o_dp.HssType() == "LOWBAT") {
							i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
							s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
						}
						
						! SMOKE_DETECTOR_TEAM
						! ROTARY_HANDLE_SENSOR
						! SHUTTER_CONTACT
						! SWITCH
						if (o_dp.HssType() == "STATE") {
							if (o_object.HssType() == "WATERDETECTIONSENSOR") {
								i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
								s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
							}
							if (o_object.HssType() == "SMOKE_DETECTOR_TEAM") {
								i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
								s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
							}
							if (o_object.HssType() == "SENSOR_FOR_CARBON_DIOXIDE") {
								i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
								s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
							}
						} ! STATE

						! POWER
						if (o_dp.HssType() == "U_SOURCE_FAIL") {
							i_errors_misc = i_errors_misc + (!b_confirmed).ToInteger();
							s_errors_new = s_errors_new #  o_object.ID() # ":" # s_dp # tab;
						} ! U_SOURCE_FAIL

					} ! HSSDP
					
				}

			}
			s_errors_new = s_errors_new;
			o_confirmed.State (s_confirmed_new);
			o_counter.State (i_errors_batt # ':' # i_errors_comm # ':' # i_errors_conf # ':' # i_errors_misc);
		}

		if (s_errors_new != s_errors_old) {
			o_errors.State (s_errors_new);
			WriteLine ('if (window.location.pathname.match (/[^\/]*$/) == "errors.cgi") { ');
			WriteLine ('  jumpto(\'errors.cgi?reload=true\');');
			WriteLine ('}');
		}
		WriteLine ('var errors_count = document.getElementById("errors_count");');
		WriteLine ('errors_count.innerHTML = \'<span class="left">Batt.</span><span class="right">' # i_errors_batt # '</span><br>' #
		                                      '<span class="left">Komm.</span><span class="right">' # i_errors_comm # '</span><br>' #
											  '<span class="left">Konfig.</span><span class="right">' # i_errors_conf # '</span><br>' #
											  '<span class="left">Sonst.</span><span class="right">' # i_errors_misc # '</span>\';');
		
	}]
	
	puts -nonewline $res(STDOUT)

}
