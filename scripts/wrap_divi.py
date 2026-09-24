"""Wrap a page code file into Divi content: one Code section + ContactaPro form section.
Usage: python3 scripts/wrap_divi.py <code.html> "<Admin Label>" "<ref value>" <out.txt>"""
import sys,urllib.parse
code=open(sys.argv[1]).read().replace('\n','').replace('\r','')
assert '[' not in code and ']' not in code
lab=sys.argv[2]; ref=urllib.parse.quote(sys.argv[3])
c=(f'[et_pb_section fb_built="1" admin_label="{lab} Redesign" _builder_version="4.27.5" _module_preset="default" custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{{}}"]'
 '[et_pb_row _builder_version="4.27.5" _module_preset="default" width="100%" max_width="100%" custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{}"]'
 '[et_pb_column type="4_4" _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"]'
 f'[et_pb_code admin_label="{lab} Page" _builder_version="4.27.5" _module_preset="default" custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{{}}"]'+code+'[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]'
 '[et_pb_section fb_built="1" admin_label="Contact Form" _builder_version="4.17.4" _module_preset="default" custom_margin="0px||0px||false|false" custom_padding="0px||0px||true|false" global_colors_info="{}"][et_pb_row column_structure="1_5,3_5,1_5" _builder_version="4.17.4" _module_preset="default" global_colors_info="{}"][et_pb_column type="1_5" _builder_version="4.17.4" _module_preset="default" global_colors_info="{}"][/et_pb_column][et_pb_column type="3_5" _builder_version="4.17.4" _module_preset="default" global_colors_info="{}"][et_pb_code _builder_version="4.27.4" _module_preset="default" global_colors_info="{}"]'
 f"<iframe aria-label='Contact a Pro' frameborder=\"0\" style=\"height:500px;width:99%;border:none;\" src='https://forms.goclearvista.com/clearvista/form/ContactaPro/formperma/O7JlkryEddXItSwvNTodTFWnAsHCI4_YceBLw9NwsmE?ref={ref}'></iframe>"
 '[/et_pb_code][/et_pb_column][et_pb_column type="1_5" _builder_version="4.17.4" _module_preset="default" global_colors_info="{}"][/et_pb_column][/et_pb_row][/et_pb_section]')
open(sys.argv[4],'w').write(c); print(len(c))
