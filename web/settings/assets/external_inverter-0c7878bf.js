import{_ as c,q as n,l as d,m as p,A as o,K as s,v as a,u as l,x as u}from"./vendor-b78ff8c0.js";import"./vendor-sortablejs-116030fd.js";const _={name:"DeviceE3dcExternalInverter",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},deviceId:{default:void 0},componentId:{required:!0}},methods:{updateConfiguration(e,t=void 0){this.$emit("update:configuration",{value:e,object:t})}}},f={class:"device-e3dc-external-inverter"},m={class:"small"};function v(e,t,b,g,h,x){const r=n("openwb-base-heading"),i=n("openwb-base-alert");return d(),p("div",f,[o(r,null,{default:s(()=>[a(" Einstellungen für externe E3DC Wechselrichter "),l("span",m,"(Modul: "+u(e.$options.name)+")",1)]),_:1}),o(i,{subtype:"info"},{default:s(()=>[a(" Diese Komponente benötigt keine Einstellungen. ")]),_:1})])}const $=c(_,[["render",v],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/e3dc/external_inverter.vue"]]);export{$ as default};