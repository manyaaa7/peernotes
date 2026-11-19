from django.core.management.base import BaseCommand
from notes.models import Course

CURRICULUM_DATA = [
    # 1st Year Common Courses (Semesters 1 & 2)
    ('COMMON', 1, False, [
        ('EBS101', 'Physics for Engineers'),
        ('EBS103', 'Chemistry for Engineers'),
        ('EBS102', 'Engineering Mathematics I'),
        ('EES101', 'Engineering Mechanics'),
        ('EES102', 'Digital Electronics'),
        ('EES103', 'Algorithmic Thinking & Programming'),
        ('EES104', 'Basic Electrical Engineering'),
        ('EHC101', 'Engineering Economics'),
    ]),
    ('COMMON', 2, False, [
        ('EBS104', 'Engineering Mathematics II'),
        ('EES105', 'Programming for Problem Solving'),
        ('EHC102', 'Ideation & Design Thinking'),
    ]),

    # B.Tech. Computer Science & Engineering (ECS)
    ('ECS', 3, False, [
        ('ECS201', 'Discrete Mathematics'),
        ('ECS202', 'Data Structures & Algorithms'),
        ('ECS203', 'Computer Organisation & Design'),
        ('ECS204', 'Software Engineering'),
    ]),
    ('ECS', 4, False, [
        ('ECS205', 'Design and Analysis of Algorithms'),
        ('ECS206', 'Database Management Systems'),
        ('ECS207', 'Systems Programming & Compilers'),
        ('ECS208', 'Operating Systems'),
    ]),
    ('ECS', 5, False, [
        ('ECS301', 'Computer Networks'),
        ('ECS302', 'Introduction to Cyber Security'),
        ('ECS303', 'Web Technologies'),
    ]),
    ('ECS', 6, False, [
        ('ECS304', 'Cloud Computing'),
        ('ECS305', 'Cryptography & Network Security'),
        ('ECS306', 'Introduction to AI & ML'),
    ]),
    ('ECS', 7, False, [
        ('ECS401', 'Deep Learning'),
        ('ECS402', 'Generative AI'),
    ]),

    # B.Tech. Computer Science & Artificial Intelligence (EAI)
    ('EAI', 3, False, [
        ('EAI201', 'Discrete Mathematics'),
        ('EAI202', 'Data Structures & Algorithms'),
        ('EAI203', 'Computer Organisation & Design'),
        ('EAI204', 'Introduction to AI & ML'),
    ]),
    ('EAI', 4, False, [
        ('EAI205', 'Data Analytics & Visualisation'),
        ('EAI206', 'Database Management Systems'),
        ('EAI207', 'Mathematical Optimization'),
        ('EAI208', 'Operating Systems'),
    ]),
    ('EAI', 5, False, [
        ('EAI301', 'Computer Networks'),
        ('EAI302', 'Responsible AI'),
        ('EAI303', 'AI-powered Cybersecurity Systems'),
    ]),
    ('EAI', 6, False, [
        ('EAI304', 'Cloud Computing'),
        ('EAI305', 'Cryptography for Intelligent Systems'),
        ('EAI306', 'Natural Language Processing'),
    ]),
    ('EAI', 7, False, [
        ('EAI401', 'Deep Learning'),
        ('EAI402', 'Generative AI'),
    ]),

    # B.Tech. Electrical Engineering & Computer Science (EEC)
    ('EEC', 3, False, [
        ('EEC201', 'Electrical Circuits and Networks'),
        ('EEC202', 'Computer Organization and Design'),
        ('EEC203', 'Data Structures and Algorithms'),
        ('EEC204', 'Electromagnetic Field Theory'),
        ('EEC205', 'Microcontrollers and Applications'),
    ]),
    ('EEC', 4, False, [
        ('EEC206', 'Power and Energy Engineering'),
        ('EEC207', 'Signals and Systems'),
        ('EEC208', 'Analog Electronics'),
    ]),
    ('EEC', 5, False, [
        ('EEC301', 'Power Electronics'),
        ('EEC302', 'Control Engineering'),
        ('EEC303', 'Digital Signal Processing'),
        ('EEC304', 'Embedded Systems Design'),
    ]),
    ('EEC', 6, False, [
        ('EEC305', 'Operating Systems'),
        ('EEC306', 'Electric Drives and Motion Control'),
        ('EEC307', 'Introduction to AI and ML'),
    ]),
    ('EEC', 7, False, [
        ('EEC308', 'Introduction to Robotics'),
    ]),

    # B.Tech. Electronics Engineering - VLSI & Embedded Systems (EVE)
    ('EVE', 3, False, [
        ('EVE201', 'Electrical Circuits and Networks'),
        ('EVE202', 'Computer Organization and Design'),
        ('EVE203', 'Data Structures and Algorithms'),
        ('EVE204', 'Electromagnetic Field Theory'),
        ('EVE205', 'Microcontrollers and Applications'),
    ]),
    ('EVE', 4, False, [
        ('EVE206', 'Digital IC Design'),
        ('EVE207', 'Signals and Systems'),
        ('EVE208', 'Analog Electronics'),
    ]),
    ('EVE', 5, False, [
        ('EVE301', 'HDL-based Design'),
        ('EVE302', 'Control Engineering'),
        ('EVE303', 'Embedded Systems Design'),
        ('EVE304', 'Digital Signal Processing'),
    ]),
    ('EVE', 6, False, [
        ('EVE305', 'VLSI Technology'),
        ('EVE306', 'PCB Design'),
    ]),

    # B.Tech. Electronics & Communication Engineering (ECE)
    ('ECE', 3, False, [
        ('ECE201', 'Electrical Circuits and Networks'),
        ('ECE202', 'Fundamentals of Communication System'),
        ('ECE203', 'Random Signals and Noise'),
        ('ECE204', 'Electromagnetic Field Theory'),
        ('ECE205', 'Microcontrollers and Applications'),
    ]),
    ('ECE', 4, False, [
        ('ECE206', 'Digital System Design using HDL'),
        ('ECE207', 'Signals and Systems'),
        ('ECE208', 'Analog Electronics'),
    ]),
    ('ECE', 5, False, [
        ('ECE301', 'Antennas and Wave Propagation'),
        ('ECE302', 'Control Engineering'),
        ('ECE303', 'Digital Signal Processing'),
        ('ECE304', 'Embedded Systems Design'),
    ]),
    ('ECE', 6, False, [
        ('ECE305', 'Image Processing and Pattern Recognition'),
        ('ECE306', 'PCB Design'),
        ('ECE307', 'Introduction to AI & ML'),
    ]),
    ('ECE', 7, False, [
        ('ECE308', 'Communication Networks'),
    ]),

    # B.Tech. Mechanical & Aerospace Engineering (EMA)
    ('EMA', 3, False, [
        ('EMA201', 'Nature and Properties of Materials'),
        ('EMA202', 'Sustainability Engineering'),
        ('EMA203', 'Basic Thermodynamics'),
        ('EMA204', 'Mechanics of Deformable Bodies'),
        ('EMA205', 'Introduction to Aerospace Engineering'),
    ]),
    ('EMA', 4, False, [
        ('EMA206', 'Manufacturing Science and Technology'),
        ('EMA207', 'Theory of Mechanisms and Machine'),
        ('EMA208', 'Fluid Mechanics & Machines'),
    ]),
    ('EMA', 5, False, [
        ('EMA301', 'Design of Machine Elements'),
        ('EMA302', 'Aerodynamics'),
        ('EMA303', 'Heat and Mass Transfer'),
        ('EMA304', 'Vibration and Control'),
    ]),
    ('EMA', 6, False, [
        ('EMA305', 'Computational Fluid Dynamics'),
        ('EMA306', 'Introduction to Machine Learning'),
    ]),
    ('EMA', 7, False, [
        ('EMA401', 'Design of FRP and Composites'),
        ('EMA402', 'Flight Mechanics'),
    ]),

    # B.Tech. Civil Engineering (ECV)
    ('ECV', 3, False, [
        ('ECV201', 'Mechanics of Deformable Bodies'),
        ('ECV202', 'Building Materials and Construction'),
        ('ECV203', 'Surveying'),
        ('ECV204', 'Sustainability Engineering'),
        ('ECV205', 'Concrete Technology'),
    ]),
    ('ECV', 4, False, [
        ('ECV206', 'Analysis of Structural Systems'),
        ('ECV207', 'Soil Mechanics & Foundation Engineering'),
        ('ECV208', 'Hydraulic Engineering'),
    ]),
    ('ECV', 5, False, [
        ('ECV301', 'Design of RC Structures & Detailing'),
        ('ECV302', 'Transportation Systems Engineering'),
        ('ECV303', 'Public Health Engineering'),
    ]),
    ('ECV', 6, False, [
        ('ECV304', 'Design of Steel Structures & Detailing'),
        ('ECV305', 'Computational Hydrology'),
        ('ECV306', 'Introduction to Machine Learning'),
    ]),
    ('ECV', 7, False, [
        ('ECV401', 'Quantity Estimation and Costing'),
        ('ECV402', 'Building Information Modelling'),
    ]),

    # B.Tech. Robotics & Automation (ERA)
    ('ERA', 3, False, [
        ('ERA201', 'Introduction to Robotics and Automation'),
        ('ERA202', 'Theory of Machines and Mechanisms'),
        ('ERA203', 'Analog and Digital Electronics'),
        ('ERA204', 'Materials and Smart Materials'),
        ('ERA205', 'Mechanical System Design'),
    ]),
    ('ERA', 4, False, [
        ('ERA206', 'Kinematics and Dynamics of Robotic Systems'),
        ('ERA207', 'Microcontrollers and Embedded Systems'),
        ('ERA208', 'Basics of Control Systems'),
    ]),
    ('ERA', 5, False, [
        ('ERA301', 'Electromechanical Energy Conversion'),
        ('ERA302', 'Micro-Electro-Mechanical Systems'),
        ('ERA303', 'Sensors and Actuators'),
        ('ERA304', 'Introduction to AI ML'),
    ]),
    ('ERA', 6, False, [
        ('ERA305', 'Industrial Automation (PLC & SCADA)'),
        ('ERA306', 'Power Converters and Drives'),
    ]),
    ('ERA', 7, False, [
        ('ERA401', 'Smart Manufacturing and Industry 4.0'),
        ('ERA402', 'ROS (Robot Operating System)'),
    ]),
]


class Command(BaseCommand):
    help = 'Seeds official Chanakya University B.Tech courses'

    def handle(self, *args, **kwargs):
        created_count = 0
        for branch, semester, is_elective, courses in CURRICULUM_DATA:
            for code, title in courses:
                _, created = Course.objects.get_or_create(
                    code=code, branch=branch, semester=semester,
                    defaults={'title': title, 'is_elective': is_elective}
                )
                if created:
                    created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created_count} official Chanakya University courses!'))