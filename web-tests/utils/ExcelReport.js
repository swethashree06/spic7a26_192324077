const ExcelJS = require('exceljs');
const fs = require('fs-extra');
const path = require('path');
const moment = require('moment');

class ExcelReport {
    constructor() {
        this.workbook = new ExcelJS.Workbook();
        this.sheet = this.workbook.addWorksheet('Test Results');
        this.sheet.columns = [
            { header: 'Test Case ID', key: 'id', width: 15 },
            { header: 'Module', key: 'module', width: 15 },
            { header: 'Test Name', key: 'name', width: 30 },
            { header: 'Status', key: 'status', width: 10 },
            { header: 'Execution Time', key: 'time', width: 15 },
            { header: 'Screenshot Path', key: 'screenshot', width: 50 },
            { header: 'Remarks', key: 'remarks', width: 30 }
        ];
    }

    async addResult(data) {
        this.sheet.addRow({
            id: data.id,
            module: data.module,
            name: data.name,
            status: data.status,
            time: data.time,
            screenshot: data.screenshot,
            remarks: data.remarks
        });
    }

    async saveReport() {
        const timestamp = moment().format('YYYY-MM-DD_HH-mm-ss');
        const fileName = `TestReport_${timestamp}.xlsx`;
        const filePath = path.join(process.cwd(), 'reports/excel', fileName);
        await fs.ensureDir(path.dirname(filePath));
        await this.workbook.xlsx.writeFile(filePath);
        console.log(`Excel report generated: ${filePath}`);
    }
}

module.exports = new ExcelReport();
