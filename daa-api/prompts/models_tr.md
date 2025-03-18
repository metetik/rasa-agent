**Görev:** Rasa ile geliştirilen bir chatbot uygulamasının FastAPI backend'i için `models.py` dosyasını oluştur.

**Bağlam:**

*   Chatbot uygulamasının temel mimarisi Rasa'dır.
*   Backend API'si FastAPI ile geliştirilecektir.
*   Veritabanı etkileşimi için SQLModel kullanılacaktır.

**Girdi:**

Aşağıda, uygulamanın gereksinim dökümanı ve kullanılacak SQLModel modellerinin listesi bulunmaktadır. Bu bilgileri kullanarak `models.py` dosyasını oluşturun.

Gereksinim dökümanı:
```markdown
# Diş Hekimi Asistanı Agent Gereksinimler

**Problem tanımı**: Küçük ve orta ölçekli diş polikliniklerinde diş hekimi asistanları hem hasta tedavisi ile ilgili görevleri yerine getirirken hem de aynı zamanda hasta randevularını yönetme, hasta bilgilerini arama gibi çok çeşitli görevler üstleniyor. Bu durum asistan için zorlayıcı olabilmektedir. Dişhekimi Assistant Agent'n görevi tüm bu süreçleri asistan ile hekim için kolaylaştırmaktır/hızlandırmaktır. Böylece hekimin ve asistanın yükü azalacak ve daha verimli bir iş alışı sağlanacaktır.

- Agent yeni bir hasta kaydı açabilmelidir.

- Agent bir hasta için yeni randevu oluşturabilmelidir.

- Agent oluşturulan randevuyu için hastaya eposta veya SMS yoluyla bildirim gönderilebilmelidir.

- Agent hastanın geçmiş tedavilerini sorgulayabilmelidir.

- Agent hasta ile ilgili bilgileri sorgulayabilidir.

- Agent hasta için tedavi planı kaydedebilmelidir.

- Agent hasta için oluşturulan tedavi planını bildirim olarak hastaya gönderebilmelidir.

- Agent hekimden teknik bilgiler alarak tedavi ile ilgili öneriler vermelidir.

- Agent hekimden aldığı görüntüleri (çoğunluklar röntgen) hekimin beklediği analizleri yapmak üzere görüntü analizi modeline gönderebilmelidir.

- Tedavi tamamlandığında hastaya yapılan işlemler ve ödeme planı ile ilgili bilgilendirme gönderilmelidir.

- Eğer randevu saatinde gecikme olacaksa hastaya bu konuda bilgilendime gönderebilmelidir.

- Hastaya yaklasan randevu ile ilgili bildirim gönderilebilmelidir.
```


SQLModel Listesi
```markdown
- Staff
	- Id
	- Name
	- Surname
	- Role 
	- ...

- Patient
	- Id
	- IdentityNumber
	- Name
	- Surname
	- Age
	- Notes
	- ...

- PatientNote
	- Id
	- Patient
	- CreateDate
	- ModifiedDate
	- Content
	- ...

- Appointment
	- Id
	- Patient
	- Dentist
	- Description
	- StartDate
	- EndDate
	- Completed
	- ...

- Agent
	- Id
	- Name
	- Model
	- ...

- TreatmentPlan
	- Id
	- Patient
	- Treatments
	- CreatedByDentist
	- CreatedDate
	- ModifiedDate
	- Agent
	- ...

- Treatment
	- Id
	- TreatmentPlan
	- Patient
	- Dentist
	- Agent
	- TreatmentNotes
	- Status
	- ModifiedDate
	- ...


- TreatmentNotes
	- Id
	- Treatment
	- Content
	- CreatedDate
	- ModifiedDate
	- Agent
	- ...

- PaymentPlan
	- Id
	- Patient
	- Description
	- CreatedBy
	- CreatedDate
	- ModifiedDate
	- Payments
	- ...

- Payment
	- Id
	- Status
	- Operation
	- Amount
	- Description
	- ...

- Image
	- Id
	- Name
	- Patient
	- CreatedBy
	- CreatedDate
	- ModifiedDate
	- ImageContent
	- ImageLink
	- Description
	- ...

- Notification
	- Id
	- NotificationType
	- Content
	- SendDate
	- ...
```

**Çıktı:**

*   `models.py` dosyasının içeriği.
*   Dosya, SQLModel kütüphanesini kullanarak tanımlanmış, ilişkisel veritabanı modellerini içermelidir.
*   Modeller arasındaki ilişkiler doğru bir şekilde tanımlanmalı ve `back_populates` gibi gerekli özellikler kullanılmalıdır.
*   Kod, Python best-practice'lerine uygun, okunabilir ve bakımı kolay olmalıdır.
*   Her modelin amacını ve önemli alanlarını kısaca açıklayan yorumlar ekleyin.

**Ek Bilgiler (İsteğe Bağlı):**

*   Kullanılacak veritabanı sistemi (örneğin, SQLite, PostgreSQL, MySQL)
*   Model ilişkilerinin karmaşıklığı hakkında ek detaylar
*   Özel gereksinimler veya kısıtlamalar

