# TeamBoard

Modern bir takım yönetimi ve görev takip uygulaması  
Vue 3 (Vite), Django REST Framework, JWT Authentication ve responsive, kullanıcı dostu arayüz 🚀

---

### 1. Giriş / Kayıt Ekranı

![Login Page]<img width="1920" height="923" alt="login" src="https://github.com/user-attachments/assets/0737f8a4-d398-4c31-ae1e-306214d2188c" />
*Kullanıcılar uygulamaya güvenli giriş yapabilir veya yeni hesap oluşturabilir.*

---

### 2. Takım Detay Sayfası

![Team Detail]<img width="1920" height="922" alt="teamDetail" src="https://github.com/user-attachments/assets/565186ed-60c7-4ec9-833d-1d8400062c03" />  
*Takım üyeleri, sahip, takım projeleri ve üye yönetimi ekranı.*

---

### 3. Proje Detay Sayfası

![Project Detail]<img width="1920" height="924" alt="projectDetail" src="https://github.com/user-attachments/assets/995187e3-e97b-48fe-8e9f-09c41103595c" /> 
*Bir projenin ayrıntılarını, açıklamasını ve tüm görevlerini görebileceğiniz sayfa.*

---

### 4. Görev (Task) Detay Sayfası

![Task Detail]<img width="1920" height="927" alt="taskDetail" src="https://github.com/user-attachments/assets/7e21c20c-31ff-45d0-9a95-8fcd25144a12" /> 
*Bir görevin sahibi, durumu ve atanmış kişisiyle detaylı incelemesi.*

---

### 5. (İsteğe Bağlı) Dashboard / Sol Menü

![Sidebar]<img width="1920" height="919" alt="profile" src="https://github.com/user-attachments/assets/276a1d6b-b540-498f-b735-29d0f27edb98" />
*Projeler, takımlar, görevler ve hızlı erişim için modern bir sol menü.*

---

## 🔥 Proje Özellikleri

- JWT tabanlı kimlik doğrulama
- Takım oluşturma, takım üyeleri ekleme/çıkarma
- Proje oluşturma, düzenleme, silme
- Görev ekleme, durum güncelleme, atama
- Responsive (mobil uyumlu) ve modern arayüz
- Yetkilere göre farklı görünüm: Admin / Member ayrımı
- Kullanıcı dostu arayüzler ve yönetilebilir yapılar

---

## 🚀 Kurulum

**Backend (Django):**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Frontend (Vue.js):

bash
Kopyala
Düzenle
cd frontend
npm install
npm run dev

⚙️ Kullanım
Localhost’ta backend’i ve frontend’i başlat.
http://localhost:5173 adresine git ve uygulamayı kullanmaya başla!

📂 Proje Yapısı
bash
Kopyala
Düzenle
/backend    # Django API & business logic
/frontend   # Vue.js SPA & arayüz


🙏 Teşekkür & İthaf
Bu proje, N2Mobil staj sürecimde Uğur Abi başta olmak üzere tüm ekibin desteğiyle geliştirilmiştir.
Fikir, mentorluk ve ilham için teşekkürler!

