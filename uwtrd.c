/* Eric Nelson
 * Fall 2013 TCSS 422 Block driver project
 * Referenced LDD's sbull driver
 */

#include <linux/kconfig.h>
#include <linux/module.h>
#include <linux/init.h> // __init and __exit
#include <linux/errno.h>
#include <linux/genhd.h>
#include <linux/blkdev.h>
#include <linux/vmalloc.h>
#include <linux/genhd.h>
#include <linux/hdreg.h>
#include <linux/fs.h>
#include <linux/bio.h>
#include <linux/string.h>
#include <linux/kdev_t.h> // MKDEV

MODULE_LICENSE("GPL");

#define DFLT_LOG_LVL KERN_WARNING
#define NUM_MINORS 8
#define DEVICE_CAPACITY_BYTES 104857600 // 100MB
#define SECTOR_SIZE 512
#define NUM_SECTORS ( ( DEVICE_CAPACITY_BYTES ) / ( SECTOR_SIZE ) )
#define MODULE_NAME "uwtrd"
#define MODULE_MAJOR 60


struct uwtrd_device {
	uint32_t size;
	uint8_t *data;
	uint8_t users;
	spinlock_t lock;
	struct request_queue *queue;
	struct gendisk *gd;
};

static void uwtrd_device_init(struct uwtrd_device*);
static void uwtrd_device_cleanup(struct uwtrd_device*);
static void uwtrd_request(struct request_queue *, struct bio *);
static void uwtrd_transfer(struct uwtrd_device *, sector_t, 
	unsigned int, char *, int write);

int uwtrd_init(void);
void uwtrd_exit(void);

int uwtrd_open(struct block_device *, fmode_t);
void uwtrd_release(struct gendisk *, fmode_t);
int uwtrd_revalidate(struct gendisk *);
int uwtrd_ioctl(struct block_device *, fmode_t, unsigned, unsigned long);
int uwtrd_getgeo(struct block_device *, struct hd_geometry*);

module_init(uwtrd_init);
module_exit(uwtrd_exit);

int uwtrd_major;
struct uwtrd_device device;

static struct block_device_operations bdops = {
	owner: THIS_MODULE,
	open: uwtrd_open,
	release: uwtrd_release,
	ioctl: uwtrd_ioctl,
	getgeo: uwtrd_getgeo,
	revalidate_disk: uwtrd_revalidate
};

static void debug(char *msg) {
	printk(DFLT_LOG_LVL MODULE_NAME ": %s", msg);
}

static void uwtrd_device_init(struct uwtrd_device *ud) {
	debug("device_init called\n");

	memset(ud, 0, sizeof (struct uwtrd_device));
	ud->gd = NULL;
	ud->queue = NULL;
	ud->size = DEVICE_CAPACITY_BYTES;
	ud->data = vmalloc(ud->size);
	if (ud->data == NULL) {
		debug("malloc faliure in device_init\n");
		return;
	}
	spin_lock_init(&ud->lock);

	ud->queue = blk_alloc_queue(GFP_KERNEL);
	if (ud->queue == NULL) {
		debug("couldn't allocate queue\n");
		goto err_free_mem;
	}
	blk_queue_make_request(ud->queue, uwtrd_request);

	ud->queue->queuedata = ud;
	
	ud->gd = alloc_disk(NUM_MINORS);
	if (ud->gd == NULL) {
		debug("couldn't allocate disk in device_init.\n");
		goto err_free_mem;
	}

	ud->gd->major = uwtrd_major;
	ud->gd->minors = NUM_MINORS;
	ud->gd->first_minor = 1;
	ud->gd->fops = &bdops;
	ud->gd->queue = ud->queue;
	ud->gd->private_data = ud;
	snprintf(ud->gd->disk_name, 32, MODULE_NAME);
	set_capacity(ud->gd, ud->size / SECTOR_SIZE);
	add_disk(ud->gd);
	return;

err_free_mem:
	uwtrd_device_cleanup(ud);
}

static void uwtrd_device_cleanup(struct uwtrd_device *ud) {
	debug("cleanup called\n");

	if (ud->queue)
		blk_cleanup_queue(ud->queue);
	if (ud->gd) {
		del_gendisk(ud->gd);
		put_disk(ud->gd);
	}
	if (ud->data)
		vfree(ud->data);

	blk_unregister_region(MKDEV(MODULE_MAJOR, 0), NUM_MINORS);
}

static void uwtrd_request(struct request_queue *rq, struct bio *bio) {
	struct uwtrd_device *ud = rq->queuedata;
	struct bio_vec *bv;
	sector_t start_sctr;
	unsigned int nr_sctrs_to_trnsfr;
	int i;

	debug("request called\n");

	start_sctr = bio->bi_sector;

	bio_for_each_segment(bv, bio, i) {
		char *buf = __bio_kmap_atomic(bio, i);
		nr_sctrs_to_trnsfr = bv->bv_len;
		uwtrd_transfer(ud, start_sctr, nr_sctrs_to_trnsfr, buf,
			bio_data_dir(bio) == WRITE);
		start_sctr += nr_sctrs_to_trnsfr;
		__bio_kunmap_atomic(bio);
	}
	bio_endio(bio, 0);
	debug("requests ended\n");
}

static void uwtrd_transfer(struct uwtrd_device *ud, 
	sector_t start_sector, unsigned int size, char *buf, 
	int write) {
	unsigned long offset = start_sector * SECTOR_SIZE;

	debug("transfer called\n");

	if ((offset + size) > ud->size) {
		debug("bad read/write request (beyond end of disk)\n");
		return;
	}
	if (write)
		memcpy(ud->data + offset, buf, size);
	else
		memcpy(buf, ud->data + offset, size);
	debug("transfer ended\n");
}

struct kobject *uwtrd_probe(dev_t dev, int *partition, void *data) {
	// only one device, so there's only one possible gendisk.
	return get_disk(device.gd);
}

int __init uwtrd_init() {
	debug("beginning init\n");

	uwtrd_major = register_blkdev(MODULE_MAJOR, MODULE_NAME);
	if (uwtrd_major < 0) {
		debug("couldn't get major number.\n");
		return -EBUSY;
	}
	
	debug("got major number\n");

	uwtrd_device_init(&device);
	debug("initialized device\n");

	blk_register_region(MKDEV(MODULE_MAJOR, 0), NUM_MINORS, THIS_MODULE, 
		uwtrd_probe, NULL, NULL);

	debug("device finished; checking...\n");
	debug("Device:\n");
	if (device.gd == NULL)
		debug("\tgd: NULL\n");
	else
		debug("\tgd: OK\n");
	if (device.queue == NULL)
		debug("\tqueue: NULL\n");
	else
		debug("\tqueue: OK\n");

	debug("init finished\n");

	return 0;
}

void __exit uwtrd_exit() {
	debug("exit called\n");

	unregister_blkdev(uwtrd_major, MODULE_NAME);
	uwtrd_device_cleanup(&device);
	
	debug("terminated successfully\n");
}

int uwtrd_open(struct block_device *bd, fmode_t fm) {
	struct uwtrd_device *ud = bd->bd_disk->private_data;

	debug("open called\n");

	spin_lock(&ud->lock);
	ud->users++;
	spin_unlock(&ud->lock);

	return 0;
}

void uwtrd_release(struct gendisk *gd, fmode_t fm) {
	struct uwtrd_device *ud = gd->private_data;

	debug("release called\n");

	spin_lock(&ud->lock);
	ud->users--;
	spin_unlock(&ud->lock);
}

int uwtrd_revalidate(struct gendisk *gd) {
	debug("revalidate called\n");

	return 0;
}

int uwtrd_ioctl(struct block_device *bd, fmode_t fm, unsigned cmd, 
	unsigned long arg) {
	struct hd_geometry g;

	debug("ioctl called\n");

	switch (cmd) {
	case HDIO_GETGEO:
		uwtrd_getgeo(bd, &g);
		if (copy_to_user((void __user *) arg, &g, sizeof (g)))
			return -EFAULT;
		return 0;
	default:
		return -ENOTTY;
	}
}

int uwtrd_getgeo(struct block_device *bd, struct hd_geometry *geo) {
	struct uwtrd_device *ud = bd->bd_disk->private_data;

	debug("getgeo called\n");

	// I don't know the why of this bit of bit-wizardry. LDD says it gets
	// a sensible fake value for cylinders, so I'm going with it.
	geo->cylinders = (ud->size & ~0x3f) >> 6;
	geo->heads = 4;
	geo->sectors = 16;
	geo->start = 4;

	return 0;
}

// vim: noai:ts=4:sw=4

