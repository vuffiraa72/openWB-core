import{D as u}from"./HardwareInstallation-a0083e3a.js";import{_ as p,u as r,k as d,l as m,D as i,N as s,y as a}from"./vendor-f2b8aa6f.js";import"./vendor-fortawesome-71546160.js";import"./index-b0e5e618.js";import"./vendor-bootstrap-4ad604fa.js";import"./vendor-jquery-d3cb8fad.js";import"./vendor-axios-65ecee4b.js";import"./vendor-sortablejs-2f1828d0.js";import"./dynamic-import-helper-be004503.js";const c={name:"DeviceKostalPikoOld",mixins:[u]},f={class:"device-kostal-piko-old"};function v(e,o,g,_,b,k){const l=r("openwb-base-heading"),n=r("openwb-base-text-input");return d(),m("div",f,[i(l,null,{default:s(()=>[a(" Einstellungen für Kostal Piko (alte Generation) ")]),_:1}),i(n,{title:"URL",subtype:"url",required:"","model-value":e.device.configuration.url,"onUpdate:modelValue":o[0]||(o[0]=t=>e.updateConfiguration(t,"configuration.url"))},{help:s(()=>[a(' Es wird eine komplette URL inklusive Protokoll erwartet. Normalerweise ist der Wechselrichter über "http://IP" zu erreichen. ')]),_:1},8,["model-value"]),i(n,{title:"Benutzername",subtype:"user",required:"","model-value":e.device.configuration.user,"onUpdate:modelValue":o[1]||(o[1]=t=>e.updateConfiguration(t,"configuration.user"))},null,8,["model-value"]),i(n,{title:"Passwort",subtype:"password",required:"","model-value":e.device.configuration.password,"onUpdate:modelValue":o[2]||(o[2]=t=>e.updateConfiguration(t,"configuration.password"))},null,8,["model-value"])])}const N=p(c,[["render",v],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/kostal/kostal_piko_old/device.vue"]]);export{N as default};