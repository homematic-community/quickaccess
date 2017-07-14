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
    		cgi_title "Inventur - HomeMatic QuickAccess"
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
			puts {<h1>Inventur</h1>}
			
			set pin ""
			catch { import pin }

			array set res [rega_script {

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					WriteLine ('<a href="javascript:jumpto(\'index.cgi#\' + js_ianchor);"><div onclick="this.className=\'standard active\';" class="standard button">zurück</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="standard button">abmelden</div></a>');
					}

					string s_device;
					object o_device;
					integer i_devices = 0;

					string s_channel;
					object o_channel;
					integer i_channels = 0;

					string s_typelist = "";

					string s_temp;

					string lst_addresses = "";
					string idx_addresses;
					integer i_addresses;

					integer i_hss_len = 0;
					integer i_name_len = 0;

					Write ('<pre>');

					foreach(s_device, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
					  var o_device = dom.GetObject(s_device);
					  if ((o_device.Address() != "BidCoS-Wir") && (o_device.Address() != "BidCoS-RF") && 
						  (o_device.Address().Substr (0,1) != "*")) {
						i_devices = i_devices + 1;
						lst_addresses = lst_addresses # o_device.Address() # ":" # o_device.ID() # "\t";
						if (o_device.HssType().Length() > i_hss_len) {
						  i_hss_len = o_device.HssType().Length();
						}
						if (o_device.Name().Length() > i_name_len) {
						  i_name_len = o_device.Name().Length();
						}
					  }
					}

					string lst_dps;
					string idx_dps;

					string last_address = "";
					string next_address = "";

					integer i;
					string s;

					while (next_address != "ZZZZZZZZ") {
					  next_address = "ZZZZZZZZ";
					  foreach (idx_addresses, lst_addresses) {
						if ((idx_addresses > last_address) && (idx_addresses < next_address)) {
						  next_address = idx_addresses;
						}
					  }
					  if (next_address != "ZZZZZZZZ") {
						o_device = dom.GetObject(next_address.StrValueByIndex(":",1));
						lst_dps = o_device.Channels().EnumUsedIDs();
						foreach (idx_dps, lst_dps) {
						  o_channel = dom.GetObject (idx_dps);
						  s = o_device.Address();
						  i = 10 - o_device.Address().Length();
						  while (i > 0) {
							i = i - 1;
							s = s # " ";
						  }
						  s = s # " " # o_device.HssType();
						  i = i_hss_len - o_device.HssType().Length();
						  while (i > 0) {
							i = i - 1;
							s = s # " ";
						  }
						  s = s # " " # o_device.Name();
						  i = i_name_len - o_device.Name().Length();
						  while (i > 0) {
							i = i - 1;
							s = s # " ";
						  }
						  i = o_channel.Address().StrValueByIndex(":",1).ToInteger();
						  if (i < 10) {
							s = s # "  " # i;
						  } else {
							s = s # " " # i;
						  }
						  s = s # " " # o_channel.Name();
						  WriteXML (s);
						  WriteLine ('');
						}
						WriteLine ('');
						last_address = next_address;
					  }
					}
					  
					Write ('</pre>');
					
				} ! PIN
					
			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }


		}

    }


}
