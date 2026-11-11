const admin = require("firebase-admin");
const serviceAccount = require("./serviceAccountKey.json");
const budgetData = require("./budget_2570_full.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://baas-70-default-rtdb.asia-southeast1.firebasedatabase.app"
});

const db = admin.database();

async function updateDatabase() {
  try {
    await db.ref('/').set(budgetData);
    console.log("อัปเดตข้อมูลข้อมูลงบประมาณขึ้น Firebase สำเร็จเรียบร้อย!");
    process.exit(0);
  } catch (error) {
    console.error("เกิดข้อผิดพลาดในการอัปเดต:", error);
    process.exit(1);
  }
}

updateDatabase();