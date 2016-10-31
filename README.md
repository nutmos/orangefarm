# How to use Git

วิธีใช้งาน Git

### Git Clone ก็อบไฟล์จาก Git มาไว้ที่เครื่อง

1. ก็อบโค้ดนี้ไปแปะลงใน Terminal
```git clone https://github.com/nutmos/orangefarm.git```
2. จากนั้นจะได้โฟลเดอร์ใหม่ ซึ่งเป็นโฟลเดอร์ที่รวบรวมไฟล์ทั้งหมดของงาน โดยโฟลเดอร์นี้จะใช้ทำงานทั้งหมด

### ขั้นตอนการส่งไฟล์ขึ้น Git

ปกติแล้ว เมื่อเราทำไฟล์เสร็จแล้ว และต้องการจัดการโยนขึ้นไปไว้ที่ Git ก็ต้องใช้วิธีนี้

1. ใช้คำสั่ง ```git pull``` เพื่อดึงไฟล์ลงมาให้อัพเดตเป็นเวอร์ชันล่าสุดก่อน
2. ใช้คำสั่ง ```git add -A``` เพื่อเป็นการเพิ่มไฟล์ทั้งหมดลงไปในไฟล์ที่จะอัพเดตขึ้น Git
3. ใช้คำสั่ง ```git commit -m "การเปลี่ยนแปลง"``` เพื่อเป็นการสั่งบันทึกการเปลี่ยนแปลง (ขั้นนี้คือบันทึกไว้ในคอมเรา) อย่าลืมคอมเม้นท์ด้วยว่าเปลี่ยนแปลงอะไรไปบ้าง
4. ใช้คำสั่ง ```git pull``` เพื่อดึงไฟล์ลงมาอัพเดตเวอร์ชันล่าสุดก่อน ในขั้นตอนนี้จะมีการ merge ไฟล์ในเครื่อง
5. ใช้คำสั่ง ```git push``` เพื่อเป็นการส่งอัพเดตขึ้น Git

### ถ้าเกิด Conflict ตอน git pull

1. ใช้คำสั่ง ```git status``` จากนั้นก็ดูว่าไฟล์ไหนแปลก ๆ บ้าง
2. จากนั้นก็ add > commit > pull > push ตามปกติ


#guideline การทำเว็บ, การใช้ไฟล์ และการวางไฟล์

1. แท็กทั้งหมดนี้ต้องแปะไว้ในแท็ก head
```
    <script src="https://unpkg.com/react@15.3.2/dist/react.js"></script>
    <script src="https://unpkg.com/react-dom@15.3.2/dist/react-dom.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-core/5.8.34/browser.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.2.4/foundation.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.2.4/foundation.min.css">
```
2. เหนือสุดของไฟล์จะต้องมี ```{% load static %}```
3. ถ้าจะใส่ไฟล์ JavaScript เพิ่ม หรือจะเขียน script เอง ให้ใส่ไว้ท้ายเว็บก่อนปิดแท็ก html
4. ถ้าจะใส่ไฟล์ CSS เพิ่ม ให้ใส่ไว้ต้นเว็บในแท็ก head
5. ไฟล์ HTML ให้ใส่ไว้ใน template/[ชื่อแอพ] อย่าเอาไปปนกับแอพอื่น โดยใน template จะมีไฟล์เดียวเท่านั้นคือ index.html สำหรับหน้า firstpage นอกนั้นให้แยกใส่โฟลเดอร์ให้หมด
6. ไฟล์ JavaScript ให้ใส่ไว้ใน static/js ไฟล์ JavaScript จากแอพทั้งหมดจะรวมกันที่เดียว
7. ไฟล์ CSS ให้ใส่ไว้ใน static/css/[ชื่อแอพ] อย่าเอาไปปนกับแอพอื่น โดยใน static/css จะมีไฟล์เดียวเท่านั้นคือ styles.css สำหรับเป็น CSS ใช้โดยรวม นอกนั้นแยกใส่โฟลเดอร์ให้หมด

