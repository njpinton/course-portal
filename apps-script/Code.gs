/**
 * CMSC 173 Midterm Submissions Web App
 * Updated with Google Sheet roster, security fixes, and export features
 */

// ============================================
// CONFIGURATION - Edit these as needed
// ============================================
const PARENT_FOLDER_ID = '1uqd5cgcXKxlenIk6VHk_1s56Jrpy5WxZ'; // "2025-1st Sem" folder
const SEARCH_QUERY = 'subject:midterm';
const ATTACHMENT_FOLDER_NAME = 'CMSC173 Midterm Attachments';
const ROSTER_SHEET_NAME = 'CMSC173 Student Roster';

// ============================================
// INITIAL SEED DATA - Only used on first run to populate the Sheet
// After that, edit the Google Sheet directly
// ============================================
const INITIAL_ROSTER_DATA = {
  "CMSC 173A": {
    schedule: "TF 3:00-4:30",
    students: [
      { campusId: "202208888", lastName: "FEROLINO", firstName: "JILLIANE MAY", middleName: "PAREDES", email: "jpferolino@up.edu.ph", program: "BSCS" },
      { campusId: "202206072", lastName: "LIGERO", firstName: "BETTINA", middleName: "CABALLES", email: "bcligero1@up.edu.ph", program: "BSCS" },
      { campusId: "202204163", lastName: "RULETE", firstName: "JERIC ASHLEY", middleName: "SALOMES", email: "jsrulete@up.edu.ph", program: "BSCS" },
      { campusId: "202200674", lastName: "PARAGES", firstName: "PRINCESS MAE", middleName: "BRUCES", email: "pbparages@up.edu.ph", program: "BSCS" },
      { campusId: "202203153", lastName: "DEEN", firstName: "MARFRED JAMES", middleName: "PO", email: "mpdeen@up.edu.ph", program: "BSCS" },
      { campusId: "202214026", lastName: "TORRES", firstName: "JOHN ANGELO", middleName: "BALINO", email: "jbtorres6@up.edu.ph", program: "BSCS" },
      { campusId: "202201955", lastName: "JARDIO", firstName: "RENIER JAMES", middleName: "CASINILLO", email: "rcjardio@up.edu.ph", program: "BSCS" },
      { campusId: "202255018", lastName: "DEIPARINE", firstName: "LOUISE FERMIN", middleName: "DESCALLAR", email: "lddeiparine@up.edu.ph", program: "BSCS" },
      { campusId: "202255019", lastName: "MILAY", firstName: "MAXELL", middleName: "GAHIT", email: "mgmilay@up.edu.ph", program: "BSCS" },
      { campusId: "202209099", lastName: "BANUAG", firstName: "CARL LAWRENCE", middleName: "CAJEGAS", email: "ccbanuag@up.edu.ph", program: "BSCS" },
      { campusId: "202206085", lastName: "BACARRA", firstName: "DANEL LEVI", middleName: "LIBANAN", email: "dlbacarra@up.edu.ph", program: "BSCS" },
      { campusId: "202255030", lastName: "OPLADO", firstName: "AKHYRA", middleName: "SAGAYNO", email: "asoplado@up.edu.ph", program: "BSCS" },
      { campusId: "202208154", lastName: "CATARINA", firstName: "JOURDAN KEN", middleName: "DIOCAMPO", email: "jdcatarina@up.edu.ph", program: "BSCS" },
      { campusId: "202207622", lastName: "OACAN", firstName: "ANTON RAYMUND", middleName: "MENDOZA", email: "amoacan@up.edu.ph", program: "BSCS" },
      { campusId: "202009852", lastName: "FIGUEROA", firstName: "ZIEDELL ALEXANDER", middleName: "CALIX", email: "zcfigueroa@up.edu.ph", program: "BSCS" },
      { campusId: "202213715", lastName: "DONAIRE", firstName: "JED EDISON", middleName: "JANUARIO", email: "jjdonaire@up.edu.ph", program: "BSCS" },
      { campusId: "202212610", lastName: "DELASAN", firstName: "ARWIN", middleName: "VILLARIAZA", email: "avdelasan@up.edu.ph", program: "BSCS" },
      { campusId: "202212261", lastName: "WONG", firstName: "LARKHIYA JOHNNYL", middleName: "CAGA", email: "lcwong@up.edu.ph", program: "BSCS" },
      { campusId: "202208161", lastName: "SUPATAN", firstName: "RAETHAN CHRISTIAN", middleName: "REPOLLO", email: "rrsupatan@up.edu.ph", program: "BSCS" },
      { campusId: "202255009", lastName: "TILACAS", firstName: "AL GLENREY", middleName: "ANDRIN", email: "aatilacas@up.edu.ph", program: "BSCS" },
      { campusId: "202206374", lastName: "LABISTE", firstName: "JOVEN", middleName: "PRADO", email: "jplabiste@up.edu.ph", program: "BSCS" },
      { campusId: "202201270", lastName: "MESA", firstName: "CHRIZ IAN", middleName: "DE CASTRO", email: "cdmesa@up.edu.ph", program: "BSCS" },
      { campusId: "202205628", lastName: "RODRIGUEZ", firstName: "ANDREA PAULINE", middleName: "CABILAO", email: "acrodriguez4@up.edu.ph", program: "BSCS" },
      { campusId: "202255068", lastName: "VA-AY", firstName: "CAESAR ISIDRO", middleName: "NAVALES", email: "cnvaay@up.edu.ph", program: "BSMAT" },
      { campusId: "202201872", lastName: "SAGRADO", firstName: "SHELDON ARTHUR", middleName: "MALUNJAO", email: "smsagrado@up.edu.ph", program: "BSCS" }
    ]
  },
  "CMSC 173D": {
    schedule: "TF 4:30-6:00",
    students: [
      { campusId: "202213057", lastName: "VAFLOR", firstName: "ADRIAN", middleName: "PADEN", email: "apvaflor1@up.edu.ph", program: "BSCS" },
      { campusId: "202208478", lastName: "CABANOS", firstName: "LIORA ZHAUNE", middleName: "SEVILLA", email: "lscabanos@up.edu.ph", program: "BSCS" },
      { campusId: "202209903", lastName: "NUÑEZ", firstName: "BAZER TIMOTHY", middleName: "MIÑOZA", email: "bmnunez1@up.edu.ph", program: "BSCS" },
      { campusId: "202211504", lastName: "LLENES", firstName: "JON ALEXANDER", middleName: "SONZA", email: "jsllenes@up.edu.ph", program: "BSCS" },
      { campusId: "202204719", lastName: "DEE", firstName: "FRANCIS PHILIPPE", middleName: "SALIENDRA", email: "fsdee1@up.edu.ph", program: "BSCS" },
      { campusId: "202207576", lastName: "TAN", firstName: "JOSHUA DAVID", middleName: "LARGO", email: "jltan11@up.edu.ph", program: "BSCS" },
      { campusId: "202255074", lastName: "PADILLA", firstName: "KIMBERLY", middleName: "ACOSTA", email: "kapadilla@up.edu.ph", program: "BSCS" },
      { campusId: "202207738", lastName: "VISARRA", firstName: "SAMUEL CHRISTOPHER", middleName: "VILLARANTE", email: "svvisarra@up.edu.ph", program: "BSCS" },
      { campusId: "202204720", lastName: "ABELIDO", firstName: "ANNE ELOISA", middleName: "DAYDAYAN", email: "adabelido@up.edu.ph", program: "BSCS" },
      { campusId: "202206602", lastName: "MANIGO", firstName: "JULIUS", middleName: "MURILLO", email: "jmmanigo@up.edu.ph", program: "BSCS" },
      { campusId: "202255070", lastName: "ESCARRO", firstName: "REX RUSSEL", middleName: "DAVAN", email: "rdescarro@up.edu.ph", program: "BSCS" },
      { campusId: "202204722", lastName: "LAPAZ", firstName: "JERMEL", middleName: "BUGSANGIT", email: "jblapaz@up.edu.ph", program: "BSCS" },
      { campusId: "202207224", lastName: "RAMACULA", firstName: "MARY JANNIN", middleName: "SEVARE", email: "msramacula@up.edu.ph", program: "BSCS" },
      { campusId: "202212540", lastName: "CONDOR", firstName: "FIEL", middleName: "ENRIQUEZ", email: "fecondor@up.edu.ph", program: "BSCS" },
      { campusId: "202209981", lastName: "AUGUSTO", firstName: "JAMAICA RURI", middleName: "COMALING", email: "jcaugusto@up.edu.ph", program: "BSCS" },
      { campusId: "202210002", lastName: "RETUYA", firstName: "MON ANDREW", middleName: "PEREZ", email: "mpretuya@up.edu.ph", program: "BSCS" },
      { campusId: "202200950", lastName: "MAGDUGO", firstName: "GABRIEL PAUL", middleName: "ERMAC", email: "gemagdugo@up.edu.ph", program: "BSCS" },
      { campusId: "202212772", lastName: "DELA CERNA", firstName: "LYNNETH KAY", middleName: "RICAFORT", email: "lrdelacerna1@up.edu.ph", program: "BSCS" },
      { campusId: "202255081", lastName: "LOBITAÑA", firstName: "ISABELA", middleName: "MAGALLANES", email: "imlobitana@up.edu.ph", program: "BSCS" },
      { campusId: "202206099", lastName: "BAGAZIN", firstName: "CHRISTINE MAE", middleName: "CARDEÑO", email: "ccbagazin@up.edu.ph", program: "BSCS" },
      { campusId: "202255117", lastName: "PELAYO", firstName: "MARCUS RAILEY", middleName: "MANZANAL", email: "mmpelayo@up.edu.ph", program: "BSCS" },
      { campusId: "202255121", lastName: "DELA CRUZ", firstName: "LEIAN CARL", middleName: "INLAYO", email: "lidelacruz1@up.edu.ph", program: "BSCS" },
      { campusId: "202201368", lastName: "MONTAÑO", firstName: "ERL JOHN", middleName: "RAMOS", email: "ermontano@up.edu.ph", program: "BSCS" }
    ]
  },
  "CMSC 173E": {
    schedule: "MTH 3:00-4:30",
    students: [
      { campusId: "202206375", lastName: "MONTEZON", firstName: "CARLOS NIÑO", middleName: "ARMODIA", email: "camontezon@up.edu.ph", program: "BSCS" },
      { campusId: "202255128", lastName: "TUAZON", firstName: "CHRAINE PAUL", middleName: "SUICO", email: "cstuazon3@up.edu.ph", program: "BSCS" },
      { campusId: "202214023", lastName: "BUSIÑOS", firstName: "ALESSANDRA GWYNETH", middleName: "RAYO", email: "arbusinos@up.edu.ph", program: "BSCS" },
      { campusId: "202206230", lastName: "LOPEZ", firstName: "LANIEZA MARIE", middleName: "BANGA", email: "lblopez@up.edu.ph", program: "BSCS" },
      { campusId: "202211342", lastName: "ANTIG", firstName: "LANCE", middleName: "PAJARES", email: "lpantig@up.edu.ph", program: "BSCS" },
      { campusId: "202205292", lastName: "PUERTO", firstName: "JULIANA IVY", middleName: "SILOR", email: "jspuerto@up.edu.ph", program: "BSCS" },
      { campusId: "202255057", lastName: "BELLO", firstName: "NICO", middleName: "DECHETA", email: "ndbello@up.edu.ph", program: "BSCS" },
      { campusId: "202200956", lastName: "SEÑORON", firstName: "ANGEL GRACE", middleName: "ACURIN", email: "aasenoron@up.edu.ph", program: "BSCS" },
      { campusId: "202208359", lastName: "BERANDOY", firstName: "CALEB JOSH", middleName: "SALMERON", email: "csberandoy@up.edu.ph", program: "BSCS" },
      { campusId: "202255058", lastName: "BANTUGAN", firstName: "JANNA MAUREEN", middleName: "AMORA", email: "jabantugan1@up.edu.ph", program: "BSCS" },
      { campusId: "202255056", lastName: "TROCIO", firstName: "ANGELINNE", middleName: "CABONELAS", email: "actrocio1@up.edu.ph", program: "BSCS" },
      { campusId: "202208404", lastName: "ALCORDO", firstName: "RONAN ZAIREL", middleName: "LOMONGGO", email: "rlalcordo@up.edu.ph", program: "BSCS" },
      { campusId: "201806815", lastName: "GIBALAY", firstName: "BON STEVE", middleName: "LABESORES", email: "blgibalay@up.edu.ph", program: "BSCS" },
      { campusId: "202200960", lastName: "ALQUICER", firstName: "RANDALL", middleName: "APOLINARIO", email: "raalquicer@up.edu.ph", program: "BSCS" },
      { campusId: "202255011", lastName: "CACEREZ", firstName: "JASMINE", middleName: "CORONEL", email: "jccacerez@up.edu.ph", program: "BSCS" },
      { campusId: "202109459", lastName: "ARAÑAS", firstName: "ANDRE MILAN", middleName: "ABAD", email: "aaaranas@up.edu.ph", program: "BSST" },
      { campusId: "202106052", lastName: "HIMAYA", firstName: "DOMINIQUE ALFRED", middleName: "DESABELLE", email: "ddhimaya@up.edu.ph", program: "BSCS" },
      { campusId: "202113547", lastName: "DINOPOL", firstName: "JONEL", middleName: "LISONDRA", email: "jldinopol@up.edu.ph", program: "BSCS" },
      { campusId: "202107336", lastName: "LUMACAD", firstName: "RAEN CLARK", middleName: "CALUNSAG", email: "rclumacad@up.edu.ph", program: "BSCS" }
    ]
  }
};

// ============================================
// ROSTER SHEET MANAGEMENT
// ============================================

/**
 * Get the parent folder for all CMSC173 files
 */
function getParentFolder() {
  return DriveApp.getFolderById(PARENT_FOLDER_ID);
}

/**
 * Get or create the student roster Google Sheet
 * @returns {Spreadsheet} The roster spreadsheet
 */
function getOrCreateRosterSheet() {
  const parentFolder = getParentFolder();

  // Search for existing sheet in the parent folder
  const files = parentFolder.getFilesByName(ROSTER_SHEET_NAME);
  if (files.hasNext()) {
    const file = files.next();
    return SpreadsheetApp.openById(file.getId());
  }

  // Create new spreadsheet
  const spreadsheet = SpreadsheetApp.create(ROSTER_SHEET_NAME);
  const file = DriveApp.getFileById(spreadsheet.getId());

  // Move to parent folder
  file.moveTo(parentFolder);

  // Initialize with seed data
  initializeRosterSheet(spreadsheet);

  Logger.log('Created new roster sheet: ' + spreadsheet.getUrl());
  return spreadsheet;
}

/**
 * Initialize the roster sheet with seed data
 * @param {Spreadsheet} spreadsheet - The spreadsheet to initialize
 */
function initializeRosterSheet(spreadsheet) {
  const sheet = spreadsheet.getActiveSheet();
  sheet.setName('Students');

  // Set headers
  const headers = ['Section', 'Schedule', 'Campus ID', 'Last Name', 'First Name', 'Middle Name', 'Email', 'Program'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight('bold');
  headerRange.setBackground('#667eea');
  headerRange.setFontColor('white');

  // Add data rows
  const rows = [];
  for (const sectionName in INITIAL_ROSTER_DATA) {
    const section = INITIAL_ROSTER_DATA[sectionName];
    for (const student of section.students) {
      rows.push([
        sectionName,
        section.schedule,
        student.campusId,
        student.lastName,
        student.firstName,
        student.middleName,
        student.email,
        student.program
      ]);
    }
  }

  if (rows.length > 0) {
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }

  // Auto-resize columns
  for (let i = 1; i <= headers.length; i++) {
    sheet.autoResizeColumn(i);
  }

  // Freeze header row
  sheet.setFrozenRows(1);

  // Add filter
  sheet.getRange(1, 1, rows.length + 1, headers.length).createFilter();
}

/**
 * Get the student roster from the Google Sheet
 * @returns {Object} Roster data in the same format as the original constant
 */
function getStudentRosterFromSheet() {
  const spreadsheet = getOrCreateRosterSheet();
  const sheet = spreadsheet.getSheetByName('Students');

  if (!sheet) {
    Logger.log('Students sheet not found, returning empty roster');
    return {};
  }

  const data = sheet.getDataRange().getValues();
  if (data.length <= 1) {
    return {}; // Only headers, no data
  }

  const roster = {};

  // Skip header row (index 0)
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const sectionName = row[0];
    const schedule = row[1];
    const campusId = row[2];
    const lastName = row[3];
    const firstName = row[4];
    const middleName = row[5];
    const email = row[6];
    const program = row[7];

    // Skip empty rows
    if (!sectionName || !email) continue;

    // Initialize section if not exists
    if (!roster[sectionName]) {
      roster[sectionName] = {
        schedule: schedule,
        students: []
      };
    }

    roster[sectionName].students.push({
      campusId: String(campusId),
      lastName: lastName,
      firstName: firstName,
      middleName: middleName,
      email: email,
      program: program
    });
  }

  return roster;
}

/**
 * Get the URL of the roster sheet (useful for finding it)
 * @returns {string} The URL of the roster sheet
 */
function getRosterSheetUrl() {
  const spreadsheet = getOrCreateRosterSheet();
  return spreadsheet.getUrl();
}

/**
 * Manual function to re-initialize the roster sheet with seed data
 * WARNING: This will overwrite existing data!
 */
function resetRosterSheet() {
  const spreadsheet = getOrCreateRosterSheet();
  const sheet = spreadsheet.getSheetByName('Students');
  if (sheet) {
    sheet.clear();
    initializeRosterSheet(spreadsheet);
    Logger.log('Roster sheet has been reset with seed data');
  }
}

// ============================================
// WEB APP
// ============================================

/**
 * Serve the web app
 */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('CMSC 173 Midterm Submissions')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Sanitize text to prevent XSS
 * @param {string} text - Text to sanitize
 * @returns {string} Sanitized text
 */
function sanitizeText(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

/**
 * Get dashboard data by checking Drive folders
 */
function getDashboardData() {
  try {
    const folderMap = getDriveFolderMap();
    const STUDENT_ROSTER = getStudentRosterFromSheet();

    const sections = [];
    let totalStudents = 0;
    let totalSubmitted = 0;

    for (const sectionName in STUDENT_ROSTER) {
      const sectionData = STUDENT_ROSTER[sectionName];
      const students = [];

      for (const student of sectionData.students) {
        const email = student.email.toLowerCase().trim();
        const folderData = folderMap[email];
        const submitted = !!folderData && folderData.fileCount > 0;

        students.push({
          name: `${student.firstName} ${student.lastName}`,
          email: student.email,
          campusId: student.campusId,
          program: student.program,
          submitted: submitted,
          submissionDate: folderData ? folderData.date : null,
          attachmentCount: folderData ? folderData.fileCount : 0,
          folderUrl: folderData ? folderData.folderUrl : null,
          files: folderData ? folderData.files : []
        });

        totalStudents++;
        if (submitted) totalSubmitted++;
      }

      // Sort by last name
      students.sort((a, b) => a.name.split(' ').pop().localeCompare(b.name.split(' ').pop()));

      const submittedCount = students.filter(s => s.submitted).length;

      sections.push({
        name: sectionName,
        schedule: sectionData.schedule,
        students: students,
        total: students.length,
        submitted: submittedCount
      });
    }

    return {
      success: true,
      sections: sections,
      summary: {
        totalStudents: totalStudents,
        totalSubmitted: totalSubmitted,
        totalPending: totalStudents - totalSubmitted,
        submissionRate: totalStudents > 0 ? Math.round((totalSubmitted / totalStudents) * 100) : 0
      },
      rosterSheetUrl: getRosterSheetUrl()
    };
  } catch (e) {
    Logger.log('Error in getDashboardData: ' + e.message);
    return {
      success: false,
      error: e.message,
      sections: [],
      summary: { totalStudents: 0, totalSubmitted: 0, totalPending: 0, submissionRate: 0 }
    };
  }
}

/**
 * Get list of students who have submitted (for export to other apps)
 * Reads directly from Drive folders
 * @param {string} format - 'csv' or 'txt'
 * @returns {Object} Result with file content and metadata
 */
function getSubmittedStudentsList(format) {
  try {
    // Validate format parameter
    if (!format || !['csv', 'txt', 'json'].includes(format)) {
      format = 'csv';
    }

    const folderMap = getDriveFolderMap();
    const STUDENT_ROSTER = getStudentRosterFromSheet();
    const submittedStudents = [];

    // Build list of submitted students with full details
    for (const sectionName in STUDENT_ROSTER) {
      const sectionData = STUDENT_ROSTER[sectionName];

      for (const student of sectionData.students) {
        const email = student.email.toLowerCase().trim();
        const folderData = folderMap[email];

        if (folderData && folderData.fileCount > 0) {
          submittedStudents.push({
            section: sectionName,
            schedule: sectionData.schedule,
            campusId: student.campusId,
            lastName: student.lastName,
            firstName: student.firstName,
            middleName: student.middleName,
            fullName: `${student.firstName} ${student.middleName} ${student.lastName}`,
            email: student.email,
            program: student.program,
            submissionDate: folderData.date || 'Unknown',
            fileCount: folderData.fileCount,
            folderUrl: folderData.folderUrl,
            files: folderData.files.map(f => f.name).join('; ')
          });
        }
      }
    }

    // Sort by section, then last name
    submittedStudents.sort((a, b) => {
      if (a.section !== b.section) return a.section.localeCompare(b.section);
      return a.lastName.localeCompare(b.lastName);
    });

    let content = '';
    let filename = '';
    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd_HHmm');

    if (format === 'csv') {
      // CSV format
      const headers = ['Section', 'Schedule', 'Campus ID', 'Last Name', 'First Name', 'Middle Name', 'Email', 'Program', 'Submission Date', 'File Count', 'Folder URL', 'Files'];
      const rows = submittedStudents.map(s => [
        s.section,
        s.schedule,
        s.campusId,
        s.lastName,
        s.firstName,
        s.middleName,
        s.email,
        s.program,
        s.submissionDate,
        s.fileCount,
        s.folderUrl,
        s.files
      ]);

      content = [headers, ...rows]
        .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        .join('\n');
      filename = `cmsc173_submissions_${timestamp}.csv`;

    } else if (format === 'txt') {
      // Plain text format - simple list for other apps
      const lines = [
        `CMSC 173 Midterm Submissions - Exported ${timestamp}`,
        `Total Submitted: ${submittedStudents.length} students`,
        '='.repeat(60),
        ''
      ];

      let currentSection = '';
      for (const s of submittedStudents) {
        if (s.section !== currentSection) {
          currentSection = s.section;
          lines.push(`\n[${s.section}] - ${s.schedule}`);
          lines.push('-'.repeat(40));
        }
        lines.push(`${s.campusId} | ${s.lastName}, ${s.firstName} ${s.middleName} | ${s.email} | ${s.submissionDate} | ${s.fileCount} file(s)`);
      }

      content = lines.join('\n');
      filename = `cmsc173_submissions_${timestamp}.txt`;

    } else if (format === 'json') {
      // JSON format - for programmatic use
      content = JSON.stringify({
        exportDate: timestamp,
        totalSubmitted: submittedStudents.length,
        students: submittedStudents
      }, null, 2);
      filename = `cmsc173_submissions_${timestamp}.json`;
    }

    return {
      success: true,
      content: content,
      filename: filename,
      format: format,
      totalSubmitted: submittedStudents.length,
      timestamp: timestamp
    };

  } catch (e) {
    Logger.log('Error in getSubmittedStudentsList: ' + e.message);
    return {
      success: false,
      error: e.message
    };
  }
}

/**
 * Parse date from filename (format: yyyy-MM-dd_HHmm_...)
 */
function parseDateFromFilename(filename) {
  const match = filename.match(/^(\d{4})-(\d{2})-(\d{2})_(\d{2})(\d{2})/);
  if (!match) return null;

  const year = parseInt(match[1]);
  const month = parseInt(match[2]) - 1; // JS months are 0-indexed
  const day = parseInt(match[3]);
  const hour = parseInt(match[4]);
  const minute = parseInt(match[5]);

  return new Date(year, month, day, hour, minute);
}

/**
 * Get or create the main attachments folder inside the parent folder
 */
function getOrCreateAttachmentsFolder() {
  const parentFolder = getParentFolder();

  // Search for existing folder
  const folders = parentFolder.getFoldersByName(ATTACHMENT_FOLDER_NAME);
  if (folders.hasNext()) {
    return folders.next();
  }

  // Create new folder
  return parentFolder.createFolder(ATTACHMENT_FOLDER_NAME);
}

/**
 * Get a map of email -> folder info from Drive
 */
function getDriveFolderMap() {
  const folderMap = {};

  try {
    const mainFolder = getOrCreateAttachmentsFolder();
    const studentFolders = mainFolder.getFolders();

    while (studentFolders.hasNext()) {
      const folder = studentFolders.next();
      const folderName = folder.getName();

      // Extract email from folder name "Name (email@up.edu.ph)"
      const emailMatch = folderName.match(/\(([^)]+@[^)]+)\)/);
      if (!emailMatch) continue;

      const email = emailMatch[1].toLowerCase().trim();
      const filesIterator = folder.getFiles();

      let fileCount = 0;
      let earliestDate = null;
      const files = [];

      while (filesIterator.hasNext()) {
        const file = filesIterator.next();
        const fileName = file.getName();
        fileCount++;

        // Parse date from filename, fallback to file creation date
        let fileDate = parseDateFromFilename(fileName);
        if (!fileDate) {
          fileDate = file.getDateCreated();
        }

        if (fileDate && (!earliestDate || fileDate < earliestDate)) {
          earliestDate = fileDate;
        }

        files.push({
          name: fileName,
          url: file.getUrl(),
          size: formatBytes(file.getSize())
        });
      }

      if (fileCount > 0) {
        folderMap[email] = {
          date: earliestDate ? Utilities.formatDate(earliestDate, Session.getScriptTimeZone(), 'MMM dd, yyyy hh:mm a') : null,
          fileCount: fileCount,
          folderUrl: folder.getUrl(),
          files: files
        };
      }
    }
  } catch (e) {
    Logger.log('Error in getDriveFolderMap: ' + e.message);
  }

  return folderMap;
}

/**
 * Get stats for the Submissions tab (still uses Gmail)
 */
function getStats() {
  try {
    const threads = GmailApp.search(SEARCH_QUERY + ' newer_than:60d', 0, 100); // Limit to last 60 days, max 100
    let totalSubmissions = 0;
    let totalAttachments = 0;
    let unreadCount = 0;
    const uniqueEmails = new Set();

    for (const thread of threads) {
      const messages = thread.getMessages();
      for (const message of messages) {
        totalSubmissions++;
        totalAttachments += message.getAttachments().length;
        if (message.isUnread()) unreadCount++;
        uniqueEmails.add(extractEmail(message.getFrom()).toLowerCase());
      }
    }

    return {
      success: true,
      totalSubmissions: totalSubmissions,
      uniqueStudents: uniqueEmails.size,
      totalAttachments: totalAttachments,
      unreadCount: unreadCount
    };
  } catch (e) {
    Logger.log('Error in getStats: ' + e.message);
    return {
      success: false,
      error: e.message,
      totalSubmissions: 0,
      uniqueStudents: 0,
      totalAttachments: 0,
      unreadCount: 0
    };
  }
}

/**
 * Fetch all midterm submissions from Gmail
 */
function getSubmissions() {
  try {
    const threads = GmailApp.search(SEARCH_QUERY + ' newer_than:60d', 0, 100); // Limit to last 60 days, max 100
    const submissions = [];

    for (const thread of threads) {
      const messages = thread.getMessages();

      for (const message of messages) {
        const from = message.getFrom();
        const attachments = message.getAttachments();
        const attachmentData = [];

        for (const attachment of attachments) {
          attachmentData.push({
            name: attachment.getName(),
            size: formatBytes(attachment.getSize()),
            type: attachment.getContentType()
          });
        }

        // Sanitize body preview to prevent XSS
        const rawBody = message.getPlainBody() || '';
        const bodyPreview = sanitizeText(rawBody.substring(0, 300).replace(/\n/g, ' ').trim());

        submissions.push({
          id: message.getId(),
          threadId: thread.getId(),
          fromName: extractName(from),
          fromEmail: extractEmail(from),
          subject: message.getSubject(),
          date: Utilities.formatDate(message.getDate(), Session.getScriptTimeZone(), 'MMM dd, yyyy hh:mm a'),
          dateRaw: message.getDate().getTime(),
          bodyPreview: bodyPreview,
          hasAttachments: attachments.length > 0,
          attachmentCount: attachments.length,
          attachments: attachmentData,
          isRead: !message.isUnread(),
          starred: message.isStarred()
        });
      }
    }

    submissions.sort((a, b) => b.dateRaw - a.dateRaw);

    return {
      success: true,
      submissions: submissions
    };
  } catch (e) {
    Logger.log('Error in getSubmissions: ' + e.message);
    return {
      success: false,
      error: e.message,
      submissions: []
    };
  }
}

/**
 * Get or create a student folder
 */
function getOrCreateStudentFolder(mainFolder, email, name) {
  const normalizedEmail = email.toLowerCase().trim();

  const existingFolders = mainFolder.getFolders();
  while (existingFolders.hasNext()) {
    const folder = existingFolders.next();
    const folderName = folder.getName().toLowerCase();
    if (folderName.includes(normalizedEmail)) {
      return folder;
    }
  }

  const folderName = `${name} (${normalizedEmail})`;
  return mainFolder.createFolder(folderName);
}

/**
 * Format date for filename
 */
function formatDateForFilename(date) {
  return Utilities.formatDate(date, Session.getScriptTimeZone(), 'yyyy-MM-dd_HHmm');
}

/**
 * Sanitize filename
 */
function sanitizeFileName(name) {
  return name.replace(/[^a-zA-Z0-9._-]/g, '_').substring(0, 100);
}

/**
 * Save a single attachment to Drive
 * @param {string} messageId - Gmail message ID
 * @param {number} attachmentIndex - Index of attachment in the message
 */
function saveAttachmentToDrive(messageId, attachmentIndex) {
  try {
    // Input validation
    if (!messageId || typeof messageId !== 'string') {
      return { success: false, error: 'Invalid message ID' };
    }
    if (typeof attachmentIndex !== 'number' || attachmentIndex < 0) {
      return { success: false, error: 'Invalid attachment index' };
    }

    const message = GmailApp.getMessageById(messageId);
    if (!message) {
      return { success: false, error: 'Message not found' };
    }

    const attachments = message.getAttachments();

    if (attachmentIndex >= attachments.length) {
      return { success: false, error: 'Attachment not found' };
    }

    const attachment = attachments[attachmentIndex];
    const fromEmail = extractEmail(message.getFrom());
    const fromName = extractName(message.getFrom());
    const date = message.getDate();
    const dateStr = formatDateForFilename(date);

    const mainFolder = getOrCreateAttachmentsFolder();
    const studentFolder = getOrCreateStudentFolder(mainFolder, fromEmail, fromName);

    const originalName = attachment.getName();
    const lastDot = originalName.lastIndexOf('.');
    let newFileName;
    if (lastDot > 0) {
      const nameWithoutExt = originalName.substring(0, lastDot);
      const ext = originalName.substring(lastDot);
      newFileName = `${dateStr}_${sanitizeFileName(nameWithoutExt)}${ext}`;
    } else {
      newFileName = `${dateStr}_${sanitizeFileName(originalName)}`;
    }

    const file = studentFolder.createFile(attachment.copyBlob().setName(newFileName));
    // Note: Removed public sharing - files are only accessible to owner/editors

    return {
      success: true,
      url: file.getUrl(),
      downloadUrl: `https://drive.google.com/uc?export=download&id=${file.getId()}`
    };
  } catch (e) {
    Logger.log('Error in saveAttachmentToDrive: ' + e.message);
    return {
      success: false,
      error: e.message
    };
  }
}

/**
 * Save all attachments and email bodies to Drive
 */
function saveAllAttachmentsWithLinks() {
  try {
    const threads = GmailApp.search(SEARCH_QUERY + ' newer_than:60d', 0, 100); // Limit scope
    const mainFolder = getOrCreateAttachmentsFolder();
    const savedFiles = [];

    for (const thread of threads) {
      const messages = thread.getMessages();

      for (const message of messages) {
        const fromEmail = extractEmail(message.getFrom());
        const fromName = extractName(message.getFrom());
        const date = message.getDate();
        const dateStr = formatDateForFilename(date);
        const formattedDate = Utilities.formatDate(date, Session.getScriptTimeZone(), 'MMM dd, yyyy hh:mm a');

        const studentFolder = getOrCreateStudentFolder(mainFolder, fromEmail, fromName);

        // Save email body as text file
        const emailBody = message.getPlainBody();
        const subject = message.getSubject();
        const emailFileName = `${dateStr}_email_body.txt`;
        const emailContent = `From: ${message.getFrom()}\nDate: ${formattedDate}\nSubject: ${subject}\n\n${emailBody}`;

        let emailFile;
        const existingEmailFiles = studentFolder.getFilesByName(emailFileName);
        if (existingEmailFiles.hasNext()) {
          emailFile = existingEmailFiles.next();
        } else {
          emailFile = studentFolder.createFile(emailFileName, emailContent, 'text/plain');
          // Note: Removed public sharing
        }

        savedFiles.push({
          studentName: fromName,
          studentEmail: fromEmail,
          submissionDate: formattedDate,
          fileName: emailFileName,
          fileUrl: emailFile.getUrl(),
          downloadUrl: `https://drive.google.com/uc?export=download&id=${emailFile.getId()}`,
          fileSize: formatBytes(emailFile.getSize()),
          isEmailBody: true
        });

        // Save attachments
        const attachments = message.getAttachments();
        for (const attachment of attachments) {
          const originalName = attachment.getName();
          const lastDot = originalName.lastIndexOf('.');
          let newFileName;
          if (lastDot > 0) {
            const nameWithoutExt = originalName.substring(0, lastDot);
            const ext = originalName.substring(lastDot);
            newFileName = `${dateStr}_${sanitizeFileName(nameWithoutExt)}${ext}`;
          } else {
            newFileName = `${dateStr}_${sanitizeFileName(originalName)}`;
          }

          let file;
          const existingFiles = studentFolder.getFilesByName(newFileName);
          if (existingFiles.hasNext()) {
            file = existingFiles.next();
          } else {
            file = studentFolder.createFile(attachment.copyBlob().setName(newFileName));
            // Note: Removed public sharing
          }

          savedFiles.push({
            studentName: fromName,
            studentEmail: fromEmail,
            submissionDate: formattedDate,
            fileName: newFileName,
            fileUrl: file.getUrl(),
            downloadUrl: `https://drive.google.com/uc?export=download&id=${file.getId()}`,
            fileSize: formatBytes(file.getSize()),
            isEmailBody: false
          });
        }
      }
    }

    return {
      success: true,
      totalFiles: savedFiles.length,
      folderUrl: mainFolder.getUrl(),
      files: savedFiles
    };
  } catch (e) {
    Logger.log('Error in saveAllAttachmentsWithLinks: ' + e.message);
    return {
      success: false,
      error: e.message,
      totalFiles: 0,
      files: []
    };
  }
}

/**
 * Extract email from "Name <email>" format
 */
function extractEmail(from) {
  const match = from.match(/<([^>]+)>/);
  return match ? match[1] : from;
}

/**
 * Extract name from "Name <email>" format
 */
function extractName(from) {
  const match = from.match(/^([^<]+)</);
  return match ? match[1].trim().replace(/"/g, '') : from.split('@')[0];
}

/**
 * Format bytes to human readable
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}
