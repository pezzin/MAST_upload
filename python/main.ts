//% color="#ff6600" iconWidth=50 iconHeight=40
namespace robot {

    //% block="Read sensors [SENSORS] for [SECONDS] seconds, label [LABEL], upload to [URL]" blockType="command"
    //% SENSORS.shadow="string" SENSORS.defl="['pir','light']"
    //% SECONDS.shadow="number" SECONDS.defl=10
    //% LABEL.shadow="string" LABEL.defl="test"
    //% URL.shadow="string" URL.defl="https://petoiupload.vercel.app/api/data"
    export function read_and_upload_sensors(parameter: any, block: any) {
        let sensors = parameter.SENSORS.code
        let seconds = parameter.SECONDS.code
        let label = parameter.LABEL.code
        let url = parameter.URL.code

        Generator.addImport(`from sensors import *`);
        Generator.addCode(`# This block reads the sensors and uploads data directly to your server`);
        Generator.addCode(`read_sensors(${sensors}, ${seconds}, ${label}, ${url})`);
    }
}
